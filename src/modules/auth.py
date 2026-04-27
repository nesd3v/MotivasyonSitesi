from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from datetime import datetime
from src.data.database import get_db
from src.utils.helpers import hash_password, verify_password
from src.data.user import User

auth_bp = Blueprint('auth', __name__)

# Kayıt ol
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Kullanıcı adı ve şifre zorunludur.', 'danger')
            return render_template('index.html', tab='register')

        conn = get_db()
        cur = conn.cursor()

        # Kullanıcı adı alınmış mı?
        if cur.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone():
            conn.close()
            flash('Bu kullanıcı adı zaten alınmış.', 'danger')
            return render_template('index.html', tab='register')

        pw_hash = hash_password(password)
        cur.execute(
            'INSERT INTO users (username, email, password_hash, streak, last_login) VALUES (?, ?, ?, ?, ?)',
            (username, email or None, pw_hash, 1, datetime.now().isoformat())
        )
        user_id = cur.lastrowid
        conn.commit()
        conn.close()

        session['user_id'] = user_id
        session['username'] = username
        flash(f'Hoş geldin, {username}!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('index.html', tab='register')

# Giriş yap
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db()
        cur = conn.cursor()
        row = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if not row or not verify_password(password, row['password_hash']):
            conn.close()
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
            return render_template('index.html', tab='login')

        # Seriyi güncelle
        user = User(id=row['id'], username=row['username'],
                    streak=row['streak'], last_login=row['last_login'])
        yeni_seri = user.update_streak()

        cur.execute('UPDATE users SET streak = ?, last_login = ? WHERE id = ?',
                    (yeni_seri, datetime.now().isoformat(), row['id']))
        conn.commit()
        conn.close()

        session['user_id'] = row['id']
        session['username'] = row['username']
        return redirect(url_for('main.dashboard'))

    return render_template('index.html', tab='login')

# Çıkış yap
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
