import random
from flask import Blueprint, render_template, session, redirect, url_for
from src.data.database import get_db
from src.utils.helpers import format_date
from src.utils.auth import login_required

main_bp = Blueprint('main', __name__)

# Ana sayfa
@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', tab='login')

# Dashboard sayfası
@main_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    uid = session['user_id']

    user = cur.execute('SELECT * FROM users WHERE id = ?', (uid,)).fetchone()

    # Rastgele günlük alıntı seç
    tumAlıntilar = cur.execute('SELECT * FROM quotes').fetchall()
    daily_quote = random.choice(tumAlıntilar) if tumAlıntilar else None

    # Aktif hedeflerin ilk 4'ü
    active_goals = cur.execute(
        'SELECT * FROM goals WHERE user_id = ? AND is_completed = 0 ORDER BY created_at DESC LIMIT 4',
        (uid,)
    ).fetchall()

    # Son 6 bildirim
    notifications = cur.execute(
        'SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 6',
        (uid,)
    ).fetchall()

    unread_count = cur.execute(
        'SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0', (uid,)
    ).fetchone()[0]

    # Kullanıcı istatistikleri
    stats = {
        'goals_completed': cur.execute(
            'SELECT COUNT(*) FROM goals WHERE user_id = ? AND is_completed = 1', (uid,)
        ).fetchone()[0],
        'goals_total': cur.execute(
            'SELECT COUNT(*) FROM goals WHERE user_id = ?', (uid,)
        ).fetchone()[0],
        'notes_count': cur.execute(
            'SELECT COUNT(*) FROM notes WHERE user_id = ?', (uid,)
        ).fetchone()[0],
        'favorites_count': cur.execute(
            'SELECT COUNT(*) FROM favorites WHERE user_id = ?', (uid,)
        ).fetchone()[0],
        'badges_count': cur.execute(
            'SELECT COUNT(*) FROM user_badges WHERE user_id = ?', (uid,)
        ).fetchone()[0],
    }

    conn.close()

    return render_template('dashboard.html',
                           user=user,
                           daily_quote=daily_quote,
                           active_goals=active_goals,
                           notifications=notifications,
                           unread_count=unread_count,
                           stats=stats,
                           format_date=format_date)
