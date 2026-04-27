from flask import Blueprint, render_template, session
from src.data.database import get_db
from src.utils.helpers import format_date
from src.utils.auth import login_required

profile_bp = Blueprint('profile', __name__)

# Profil sayfası
@profile_bp.route('/profile')
@login_required
def profile():
    conn = get_db()
    cur = conn.cursor()
    uid = session['user_id']

    user = cur.execute('SELECT * FROM users WHERE id = ?', (uid,)).fetchone()

    # Tüm rozetler ve kazanılanlar
    tum_rozetler = cur.execute('SELECT * FROM badges').fetchall()
    kazanilan_ids = {r['badge_id'] for r in cur.execute(
        'SELECT badge_id FROM user_badges WHERE user_id = ?', (uid,)
    ).fetchall()}

    # Favori alıntılar
    favorites = cur.execute('''
        SELECT q.* FROM quotes q
        JOIN favorites f ON q.id = f.quote_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    ''', (uid,)).fetchall()

    # Tüm bildirimler
    all_notifications = cur.execute(
        'SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 20', (uid,)
    ).fetchall()

    stats = {
        'goals_total': cur.execute('SELECT COUNT(*) FROM goals WHERE user_id = ?', (uid,)).fetchone()[0],
        'goals_completed': cur.execute(
            'SELECT COUNT(*) FROM goals WHERE user_id = ? AND is_completed = 1', (uid,)
        ).fetchone()[0],
        'notes_count': cur.execute('SELECT COUNT(*) FROM notes WHERE user_id = ?', (uid,)).fetchone()[0],
        'favorites_count': len(favorites),
        'badges_count': len(kazanilan_ids),
    }

    conn.close()

    return render_template('profile.html',
                           user=user,
                           all_badges=tum_rozetler,
                           earned_ids=kazanilan_ids,
                           favorites=favorites,
                           all_notifications=all_notifications,
                           stats=stats,
                           format_date=format_date)
