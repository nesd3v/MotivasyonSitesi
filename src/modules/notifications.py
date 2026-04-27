import random
from flask import Blueprint, session, jsonify
from src.data.database import get_db
from src.utils.auth import login_required
from src.services.notification import MotivasyonBildirimi, RozetBildirimi
from src.services.badge import Badge

notifications_bp = Blueprint('notifications', __name__)

# Motivasyon bildirimi gönder
@notifications_bp.route('/send-motivation', methods=['POST'])
@login_required
def send_motivation():
    uid = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    quotes = cur.execute('SELECT * FROM quotes').fetchall()
    if not quotes:
        conn.close()
        return jsonify({'error': 'Alıntı bulunamadı'}), 404

    quote = random.choice(quotes)

    # MotivasyonBildirimi nesnesi oluşturuyorum (polimorfizm)
    bildirim = MotivasyonBildirimi(
        kategori=quote['category'],
        user_id=uid,
        title=f"Günlük Motivasyon - {quote['category'].capitalize()}",
        message=f'"{quote["text"]}" - {quote["author"]}'
    )

    cur.execute(
        'INSERT INTO notifications (user_id, title, message, type) VALUES (?, ?, ?, ?)',
        (uid, bildirim.title, bildirim.message, 'motivational')
    )
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'title': bildirim.title,
        'formatted': bildirim.format_message(),
        'quote': {'text': quote['text'], 'author': quote['author'], 'category': quote['category']}
    })

# Bildirimi okundu yap
@notifications_bp.route('/notifications/read/<int:notif_id>', methods=['POST'])
@login_required
def mark_read(notif_id):
    conn = get_db()
    conn.execute('UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?',
                 (notif_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Tümünü okundu yap
@notifications_bp.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_read():
    conn = get_db()
    conn.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Yeni rozet kazanıldı mı kontrol et
@notifications_bp.route('/check-badges', methods=['POST'])
@login_required
def check_badges():
    uid = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    user = cur.execute('SELECT streak FROM users WHERE id = ?', (uid,)).fetchone()
    istatistik = {
        'streak': user['streak'] if user else 0,
        'goals_completed': cur.execute(
            'SELECT COUNT(*) FROM goals WHERE user_id = ? AND is_completed = 1', (uid,)
        ).fetchone()[0],
        'notes_count': cur.execute('SELECT COUNT(*) FROM notes WHERE user_id = ?', (uid,)).fetchone()[0],
        'favorites_count': cur.execute('SELECT COUNT(*) FROM favorites WHERE user_id = ?', (uid,)).fetchone()[0],
    }

    tum_rozetler = cur.execute('SELECT * FROM badges').fetchall()
    kazanilan_ids = {r['badge_id'] for r in cur.execute(
        'SELECT badge_id FROM user_badges WHERE user_id = ?', (uid,)
    ).fetchall()}

    yeni_rozetler = []
    for row in tum_rozetler:
        if row['id'] not in kazanilan_ids:
            rozet = Badge(id=row['id'], name=row['name'],
                          condition_type=row['condition_type'],
                          condition_value=row['condition_value'])
            if rozet.check_condition(istatistik):
                cur.execute('INSERT OR IGNORE INTO user_badges (user_id, badge_id) VALUES (?, ?)',
                            (uid, row['id']))
                # RozetBildirimi oluşturuyorum (polimorfizm)
                bildirim = RozetBildirimi(
                    rozet_adi=row['name'],
                    user_id=uid,
                    title=f"Yeni Rozet: {row['name']}",
                    message=row['description']
                )
                cur.execute(
                    'INSERT INTO notifications (user_id, title, message, type) VALUES (?, ?, ?, ?)',
                    (uid, bildirim.title, bildirim.message, 'badge')
                )
                yeni_rozetler.append({'name': row['name'], 'icon': row['icon'], 'description': row['description']})

    conn.commit()
    conn.close()
    return jsonify({'new_badges': yeni_rozetler})
