import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.user import User
from src.data.goal import Goal
from src.data.note import Note
from src.services.badge import Badge
from src.services.notification import MotivasyonBildirimi, HedefBildirimi, RozetBildirimi
from datetime import datetime, timedelta

# ============================================================
# Model testleri
# ============================================================

def test_user_streak_ilk_giris():
    """Kullanıcı ilk kez giriş yapıyorsa seri 1 olmalı."""
    user = User(username='test', streak=0, last_login=None)
    yeni_seri = user.update_streak()
    assert yeni_seri == 1, f"Beklenen 1, gelen: {yeni_seri}"
    print("PASS: test_user_streak_ilk_giris")

def test_user_streak_ardisik_gun():
    """Dün giriş yapıldıysa seri bir artmalı."""
    dun = (datetime.now() - timedelta(days=1)).isoformat()
    user = User(username='test', streak=5, last_login=dun)
    yeni_seri = user.update_streak()
    assert yeni_seri == 6, f"Beklenen 6, gelen: {yeni_seri}"
    print("PASS: test_user_streak_ardisik_gun")

def test_user_streak_atlama():
    """2 gün giriş yoksa seri 1'e dönmeli."""
    iki_gun_once = (datetime.now() - timedelta(days=2)).isoformat()
    user = User(username='test', streak=10, last_login=iki_gun_once)
    yeni_seri = user.update_streak()
    assert yeni_seri == 1, f"Beklenen 1, gelen: {yeni_seri}"
    print("PASS: test_user_streak_atlama")

def test_goal_ilerleme_guncelle():
    """İlerleme 0-100 arasında sınırlandırılmalı."""
    hedef = Goal(title='Test Hedef', user_id=1)
    hedef.update_progress(150)
    assert hedef.progress == 100, f"Beklenen 100, gelen: {hedef.progress}"
    assert hedef.is_completed == True
    print("PASS: test_goal_ilerleme_guncelle")

def test_goal_tamamla():
    """Hedef tamamlandığında progress 100 ve is_completed True olmalı."""
    hedef = Goal(title='Test', user_id=1, progress=50)
    hedef.complete()
    assert hedef.is_completed == True
    assert hedef.progress == 100
    print("PASS: test_goal_tamamla")

def test_note_preview():
    """Uzun içerik 120 karakterde kesilmeli."""
    uzun_icerik = "A" * 200
    not_ = Note(title='Test', content=uzun_icerik, user_id=1)
    preview = not_.get_preview()
    assert len(preview) <= 123
    assert preview.endswith('...')
    print("PASS: test_note_preview")

def test_badge_kosul_kontrol():
    """Rozet koşulu doğru değerlendirilmeli."""
    rozet = Badge(name='Azimli', condition_type='streak', condition_value=7)
    yeterli = {'streak': 10, 'goals_completed': 0, 'notes_count': 0, 'favorites_count': 0}
    yetersiz = {'streak': 3, 'goals_completed': 0, 'notes_count': 0, 'favorites_count': 0}
    assert rozet.check_condition(yeterli) == True
    assert rozet.check_condition(yetersiz) == False
    print("PASS: test_badge_kosul_kontrol")

def test_polimorfizm_bildirim():
    """Her bildirim alt sınıfı farklı format_message döndürmeli (polimorfizm)."""
    mot = MotivasyonBildirimi(kategori='azim', user_id=1, title='T', message='Deneme mesajı')
    hedef_b = HedefBildirimi(hedef_adi='Spor Yap', user_id=1, title='T', message='Tebrikler!')
    rozet_b = RozetBildirimi(rozet_adi='Süper Seri', user_id=1, title='T', message='Harika!')

    assert 'azim' in mot.format_message()
    assert 'Spor Yap' in hedef_b.format_message()
    assert 'Süper Seri' in rozet_b.format_message()
    assert mot.format_message() != hedef_b.format_message()
    print("PASS: test_polimorfizm_bildirim")

def test_base_model_to_dict():
    """to_dict() hem base hem alt sınıf alanlarını içermeli (kalıtım)."""
    user = User(id=1, username='enes', streak=7)
    d = user.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'username' in d
    assert 'streak' in d
    print("PASS: test_base_model_to_dict")

# Testleri çalıştır
if __name__ == '__main__':
    print("=" * 50)
    print("MotivaSyon - Model Testleri")
    print("=" * 50)

    test_user_streak_ilk_giris()
    test_user_streak_ardisik_gun()
    test_user_streak_atlama()
    test_goal_ilerleme_guncelle()
    test_goal_tamamla()
    test_note_preview()
    test_badge_kosul_kontrol()
    test_polimorfizm_bildirim()
    test_base_model_to_dict()

    print("=" * 50)
    print("Tüm testler geçti!")
    print("=" * 50)
