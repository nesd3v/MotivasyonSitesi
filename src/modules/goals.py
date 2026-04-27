from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from src.data.database import get_db
from src.utils.auth import login_required

goals_bp = Blueprint('goals', __name__)

# Hedefler sayfası
@goals_bp.route('/goals')
@login_required
def goals():
    conn = get_db()
    cur = conn.cursor()
    uid = session['user_id']
    filtre = request.args.get('filter', 'all')

    if filtre == 'active':
        goals_list = cur.execute(
            'SELECT * FROM goals WHERE user_id = ? AND is_completed = 0 ORDER BY created_at DESC', (uid,)
        ).fetchall()
    elif filtre == 'completed':
        goals_list = cur.execute(
            'SELECT * FROM goals WHERE user_id = ? AND is_completed = 1 ORDER BY created_at DESC', (uid,)
        ).fetchall()
    else:
        goals_list = cur.execute(
            'SELECT * FROM goals WHERE user_id = ? ORDER BY is_completed ASC, created_at DESC', (uid,)
        ).fetchall()

    conn.close()
    return render_template('goals.html', goals=goals_list, filter_type=filtre)

# Hedef ekle
@goals_bp.route('/goals/add', methods=['POST'])
@login_required
def add_goal():
    uid = session['user_id']
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', 'genel')
    deadline = request.form.get('deadline', '') or None

    if not title:
        flash('Hedef başlığı zorunludur.', 'danger')
        return redirect(url_for('goals.goals'))

    conn = get_db()
    conn.execute(
        'INSERT INTO goals (user_id, title, description, category, deadline) VALUES (?, ?, ?, ?, ?)',
        (uid, title, description, category, deadline)
    )
    conn.commit()
    conn.close()

    flash('Yeni hedef eklendi!', 'success')
    return redirect(url_for('goals.goals'))

# Hedefi tamamla
@goals_bp.route('/goals/complete/<int:goal_id>', methods=['POST'])
@login_required
def complete_goal(goal_id):
    uid = session['user_id']
    conn = get_db()
    cur = conn.cursor()

    hedef = cur.execute('SELECT * FROM goals WHERE id = ? AND user_id = ?', (goal_id, uid)).fetchone()
    if hedef:
        cur.execute('UPDATE goals SET is_completed = 1, progress = 100 WHERE id = ?', (goal_id,))
        cur.execute(
            'INSERT INTO notifications (user_id, title, message, type) VALUES (?, ?, ?, ?)',
            (uid, 'Hedef Tamamlandı!', f'"{hedef["title"]}" hedefini başarıyla bitirdin!', 'goal')
        )
        conn.commit()

    conn.close()
    return jsonify({'success': True})

# İlerlemeyi güncelle
@goals_bp.route('/goals/progress/<int:goal_id>', methods=['POST'])
@login_required
def update_progress(goal_id):
    uid = session['user_id']
    ilerleme = max(0, min(100, int(request.form.get('progress', 0))))
    tamamlandi = 1 if ilerleme >= 100 else 0

    conn = get_db()
    conn.execute(
        'UPDATE goals SET progress = ?, is_completed = ? WHERE id = ? AND user_id = ?',
        (ilerleme, tamamlandi, goal_id, uid)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'progress': ilerleme, 'completed': bool(tamamlandi)})

# Hedefi sil
@goals_bp.route('/goals/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    uid = session['user_id']
    conn = get_db()
    conn.execute('DELETE FROM goals WHERE id = ? AND user_id = ?', (goal_id, uid))
    conn.commit()
    conn.close()
    return jsonify({'success': True})
