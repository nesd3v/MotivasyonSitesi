import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.core.config import Config

# Veritabanı bağlantısı açıyorum
def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Tabloları oluşturuyorum
def init_db():
    # data/ klasörü yoksa oluştur
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)

    conn = get_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        streak INTEGER DEFAULT 0,
        last_login TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT,
        category TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quote_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, quote_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (quote_id) REFERENCES quotes(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        deadline TEXT,
        is_completed INTEGER DEFAULT 0,
        progress INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        content TEXT,
        mood TEXT DEFAULT 'neutral',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        message TEXT,
        type TEXT DEFAULT 'motivational',
        is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        icon TEXT,
        condition_type TEXT,
        condition_value INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS user_badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        badge_id INTEGER,
        earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, badge_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (badge_id) REFERENCES badges(id)
    )''')

    conn.commit()
    conn.close()

# Başlangıç verilerini ekliyorum
def seed_data():
    conn = get_db()
    cur = conn.cursor()

    quotes = [
        ("Başarı, her gün tekrarlanan küçük çabaların toplamıdır.", "Robert Collier", "başarı"),
        ("Güçlü olmak zorunda değilsiniz. Sadece pes etmemek zorundasınız.", "Morgan Harper Nichols", "motivasyon"),
        ("Düştüğünde yedi kez kalk.", "Japon Atasözü", "azim"),
        ("Bugün yapabileceğini yarına bırakma.", "Benjamin Franklin", "disiplin"),
        ("Hayallerini küçük tutma. Büyük hayaller kurmanın bedeli küçük hayaller kurmanın bedeliyle aynıdır.", "Harriet Tubman", "hayaller"),
        ("Kendin ol, diğer herkes zaten alınmış.", "Oscar Wilde", "özgüven"),
        ("En büyük zafer hiç düşmemek değil, her düşüşte kalkmaktır.", "Nelson Mandela", "azim"),
        ("Seni durduran tek şey senin kendine olan güvensizliğindir.", "Anonymous", "özgüven"),
        ("Bir adım atmaya cesaret et. Basamak bile olsa.", "Audrey Hepburn", "cesaret"),
        ("Başarının sırrı başlamaktır.", "Mark Twain", "başarı"),
        ("Küçük adımlar büyük mesafeleri kat eder.", "Anonymous", "azim"),
        ("Her gün yeni bir fırsattır.", "Anonymous", "motivasyon"),
        ("Sevdiğin işi yap ve hayatında tek bir gün bile çalışmak zorunda kalmayacaksın.", "Konfüçyüs", "anlam"),
        ("Değişim zordur ama değişmemek daha da zordur.", "G.C. Lichtenberg", "değişim"),
        ("Başarı tesadüf değildir. Çok çalışmak, azim ve fedakarlık ister.", "Pelé", "başarı"),
        ("Mutluluk bir kapı değil, bir yoldur.", "Anonymous", "mutluluk"),
        ("Zaman geçmez, biz geçeriz.", "Henry Austin Dobson", "zaman"),
        ("Hayatın anlamı yeteneklerini keşfetmektir.", "W. Shakespeare", "anlam"),
        ("Başarı yolculuğa çıkmaya hazır olmakla başlar.", "Mark Twain", "başarı"),
        ("Cesaret korkunun olmadığı değil, korkuya rağmen ilerlediğin andır.", "Nelson Mandela", "cesaret"),
        ("Her sabah uyandığında güçlü olmak için bir nedenin olduğunu hatırla.", "Anonymous", "motivasyon"),
        ("Dün nerede olduğun değil, yarın nerede olmak istediğin önemlidir.", "Anonymous", "değişim"),
        ("Hayal gücü bilgiden daha önemlidir.", "Albert Einstein", "hayaller"),
        ("Disiplin özgürlüğün temelidir.", "Aristotle", "disiplin"),
        ("İnsan olmak başarısız olmak ve başarısızlığı yenmeye çalışmak demektir.", "C.S. Lewis", "azim"),
    ]

    for text, author, category in quotes:
        cur.execute('INSERT OR IGNORE INTO quotes (text, author, category) VALUES (?, ?, ?)',
                    (text, author, category))

    badges = [
        ("İlk Adım", "İlk günlük girişini yazdın!", "🎯", "notes_count", 1),
        ("Kalemini Bırakma", "5 günlük girdisi yazdın!", "📝", "notes_count", 5),
        ("Azimli Çalışan", "7 günlük giriş serisi!", "🔥", "streak", 7),
        ("Süper Seri", "30 günlük giriş serisi!", "⚡", "streak", 30),
        ("Hedef Avcısı", "İlk hedefini tamamladın!", "🏆", "goals_completed", 1),
        ("Hedef Ustası", "10 hedef tamamladın!", "🌟", "goals_completed", 10),
        ("Koleksiyoncu", "10 alıntıyı favorilere ekledin!", "❤️", "favorites_count", 10),
    ]

    for name, desc, icon, ctype, cval in badges:
        cur.execute(
            'INSERT OR IGNORE INTO badges (name, description, icon, condition_type, condition_value) VALUES (?, ?, ?, ?, ?)',
            (name, desc, icon, ctype, cval)
        )

    conn.commit()
    conn.close()
