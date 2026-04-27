import random
from flask import Blueprint, render_template, session, request, jsonify
from src.data.database import get_db
from src.utils.helpers import get_category_color
from src.utils.auth import login_required

quotes_bp = Blueprint('quotes', __name__)

# Alıntı koleksiyonu
@quotes_bp.route('/collection')
@login_required
def collection():
    conn = get_db()
    cur = conn.cursor()
    uid = session['user_id']
    kategori = request.args.get('category', '')

    if kategori:
        quotes = cur.execute('SELECT * FROM quotes WHERE category = ? ORDER BY id', (kategori,)).fetchall()
    else:
        quotes = cur.execute('SELECT * FROM quotes ORDER BY id').fetchall()

    # Favorileri set olarak alıyorum - hızlı kontrol için
    fav_ids = {row['quote_id'] for row in cur.execute(
        'SELECT quote_id FROM favorites WHERE user_id = ?', (uid,)
    ).fetchall()}

    categories = cur.execute('SELECT DISTINCT category FROM quotes ORDER BY category').fetchall()
    conn.close()

    return render_template('collection.html',
                           quotes=quotes,
                           fav_ids=fav_ids,
                           categories=categories,
                           selected_category=kategori,
                           get_category_color=get_category_color)

# Favori ekle / kaldır
@quotes_bp.route('/toggle-favorite/<int:quote_id>', methods=['POST'])
@login_required
def toggle_favorite(quote_id):
    conn = get_db()
    cur = conn.cursor()
    uid = session['user_id']

    mevcut = cur.execute(
        'SELECT id FROM favorites WHERE user_id = ? AND quote_id = ?', (uid, quote_id)
    ).fetchone()

    if mevcut:
        cur.execute('DELETE FROM favorites WHERE user_id = ? AND quote_id = ?', (uid, quote_id))
        favori_mi = False
    else:
        cur.execute('INSERT OR IGNORE INTO favorites (user_id, quote_id) VALUES (?, ?)', (uid, quote_id))
        favori_mi = True

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'is_favorite': favori_mi})

# Rastgele alıntı - AJAX için
@quotes_bp.route('/random-quote')
@login_required
def random_quote():
    conn = get_db()
    quotes = conn.execute('SELECT * FROM quotes').fetchall()
    conn.close()

    if quotes:
        q = random.choice(quotes)
        return jsonify({'text': q['text'], 'author': q['author'], 'category': q['category']})
    return jsonify({'error': 'Alıntı bulunamadı'}), 404
