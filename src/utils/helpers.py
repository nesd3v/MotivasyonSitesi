import hashlib
import secrets
from datetime import datetime

# Şifreyi hash'le - salt ile güvenli saklama
def hash_password(password):
    salt = secrets.token_hex(16)
    hash_val = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{hash_val}"

# Girilen şifreyi kayıtlı hash ile karşılaştır
def verify_password(password, stored_hash):
    try:
        salt, hash_val = stored_hash.split(':')
        computed = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed == hash_val
    except:
        return False

# Tarihi Türkçe formata çevir
def format_date(date_str):
    if not date_str:
        return 'Belirtilmemiş'
    try:
        dt = datetime.fromisoformat(str(date_str))
        aylar = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        return f"{dt.day} {aylar[dt.month - 1]} {dt.year}"
    except:
        return str(date_str)

# Ruh haline göre emoji döndür
def get_mood_emoji(mood):
    moods = {
        'happy': '😊',
        'motivated': '💪',
        'neutral': '😐',
        'tired': '😴',
        'sad': '😔'
    }
    return moods.get(mood, '😐')

# Ruh halini Türkçeye çevir
def get_mood_label(mood):
    labels = {
        'happy': 'Mutlu',
        'motivated': 'Motivasyonlu',
        'neutral': 'Normal',
        'tired': 'Yorgun',
        'sad': 'Üzgün'
    }
    return labels.get(mood, 'Normal')

# Kategori için renk döndür
def get_category_color(category):
    colors = {
        'başarı': 'primary',
        'motivasyon': 'success',
        'azim': 'warning',
        'özgüven': 'info',
        'hayaller': 'danger',
        'anlam': 'secondary',
        'disiplin': 'dark',
        'mutluluk': 'warning',
        'cesaret': 'danger',
        'değişim': 'info',
        'zaman': 'secondary',
    }
    return colors.get(category, 'primary')
