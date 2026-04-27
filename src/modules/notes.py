from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from src.data.database import get_db
from src.utils.helpers import get_mood_emoji, get_mood_label
from src.utils.auth import login_required

notes_bp = Blueprint('notes', __name__)

# Günlük sayfası
@notes_bp.route('/notes')
@login_required
def notes():
    conn = get_db()
    notes_list = conn.execute(
        'SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('notes.html', notes=notes_list,
                           get_mood_emoji=get_mood_emoji,
                           get_mood_label=get_mood_label)

# Not ekle
@notes_bp.route('/notes/add', methods=['POST'])
@login_required
def add_note():
    uid = session['user_id']
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    mood = request.form.get('mood', 'neutral')

    if not title or not content:
        flash('Başlık ve içerik zorunludur.', 'danger')
        return redirect(url_for('notes.notes'))

    conn = get_db()
    conn.execute(
        'INSERT INTO notes (user_id, title, content, mood) VALUES (?, ?, ?, ?)',
        (uid, title, content, mood)
    )
    conn.commit()
    conn.close()

    flash('Not kaydedildi!', 'success')
    return redirect(url_for('notes.notes'))

# Not sil
@notes_bp.route('/notes/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Not detayı - AJAX için
@notes_bp.route('/notes/get/<int:note_id>')
@login_required
def get_note(note_id):
    conn = get_db()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ? AND user_id = ?', (note_id, session['user_id'])
    ).fetchone()
    conn.close()

    if note:
        return jsonify({
            'id': note['id'],
            'title': note['title'],
            'content': note['content'],
            'mood': note['mood'],
            'mood_emoji': get_mood_emoji(note['mood']),
            'created_at': note['created_at']
        })
    return jsonify({'error': 'Not bulunamadı'}), 404
