# Gereksinim Analizi - MotivaSyon Uygulaması

## 1. Proje Özeti

**Proje Adı:** MotivaSyon  
**Proje Tipi:** Web Tabanlı Dinamik Motivasyon Bildirim Sistemi  
**Teknolojiler:** Python (Flask), HTML5, CSS3, JavaScript, Bootstrap 5, SQLite  
**OOP Yaklaşımı:** Kalıtım + Polimorfizm  

---

## 2. Fonksiyonel Gereksinimler

### FR-01: Kullanıcı Yönetimi
- Kullanıcı kayıt olabilmeli (kullanıcı adı, e-posta, şifre)
- Kullanıcı giriş/çıkış yapabilmeli
- Şifre güvenli hash ile saklanmalı (SHA-256 + salt)
- Kullanıcıya özel session yönetimi olmalı

### FR-02: Motivasyon Bildirimleri (Ana Özellik)
- Kullanıcı tek tıkla motivasyon bildirimi alabilmeli
- Bildirim rastgele seçilen bir alıntıdan oluşmalı
- Tarayıcı Web Notification API ile masaüstü bildirimi gönderilmeli
- Bildirimler veritabanına kaydedilmeli ve geçmişi görüntülenebilmeli

### FR-03: Hedef Takip Sistemi
- Kullanıcı yeni hedef ekleyebilmeli (başlık, açıklama, kategori, bitiş tarihi)
- Hedeflere ilerleme yüzdesi (0-100) atanabilmeli
- Hedef tamamlandığında otomatik bildirim oluşturulmalı
- Hedefler filtrelenebilmeli (Tümü / Aktif / Tamamlanan)
- Hedef silinebilmeli

### FR-04: Alıntı Koleksiyonu
- Sistemde önceden tanımlı 25 motivasyon alıntısı bulunmalı
- Alıntılar kategoriye göre filtrelenebilmeli
- Kullanıcı alıntıları favorilere ekleyip çıkarabilmeli
- Dashboard'da günlük rastgele alıntı gösterilmeli

### FR-05: Kişisel Günlük
- Kullanıcı kişisel not ekleyebilmeli (başlık, içerik, ruh hali)
- Ruh hali seçenekleri: Mutlu, Motivasyonlu, Normal, Yorgun, Üzgün
- Notlar listelenmeli ve detayı modal'da görüntülenebilmeli
- Not silinebilmeli

### FR-06: Başarı Rozet Sistemi
- Sistem önceden tanımlı rozetler içermeli
- Kullanıcı aktivitelerine göre otomatik rozet kazanılmalı
- Rozet koşulları: günlük seri, tamamlanan hedef, yazılan not, favori sayısı
- Profil sayfasında kazanılan/kazanılmayan rozetler gösterilmeli

### FR-07: Kullanıcı Profili & İstatistikler
- Toplam hedef, tamamlanan hedef, not sayısı, favori sayısı gösterilmeli
- Günlük giriş serisi gösterilmeli
- Bildirim geçmişi listelenebilmeli

### FR-08: Günlük Seri Takibi
- Her giriş yapıldığında streak (seri) hesaplanmalı
- Art arda günlerde seri artmalı, atlanırsa sıfırlanmalı

---

## 3. Fonksiyonel Olmayan Gereksinimler

| Gereksinim | Açıklama |
|------------|----------|
| Güvenlik | Şifreler hash+salt ile saklanır, CSRF koruması Flask session ile sağlanır |
| Kullanılabilirlik | Mobil uyumlu, responsive tasarım |
| Performans | Sayfa yükleme < 2 saniye |
| Sürdürülebilirlik | Modüler yapı (Blueprint + OOP) |
| Uyumluluk | Modern tarayıcılar (Chrome, Firefox, Edge) |

---

## 4. Kullanım Senaryoları (Use Case)

### UC-01: Motivasyon Bildirimi Al
- **Aktör:** Giriş yapmış kullanıcı
- **Tetikleyici:** "Motivasyon Al" butonuna basmak
- **Akış:** Buton tıkla → Sunucu rastgele alıntı seçer → Bildirim oluşturulur → Popup ve tarayıcı bildirimi gösterilir
- **Sonuç:** Bildirim DB'ye kaydedilir, kullanıcı ekranda görür

### UC-02: Hedef Ekle
- **Aktör:** Giriş yapmış kullanıcı
- **Tetikleyici:** "Yeni Hedef Ekle" formunu doldurup göndermek
- **Akış:** Form doldur → POST isteği → DB'ye kaydedilir → Hedef listesinde görünür

### UC-03: Rozet Kazan
- **Aktör:** Sistem
- **Tetikleyici:** Kullanıcı aktiviteleri (hedef tamamlama, not yazma, favori ekleme, seri)
- **Akış:** Aktivite tamamlanır → `/check-badges` AJAX çağrısı → Koşullar kontrol edilir → Yeni rozetler verilir → Popup ile bildirilir

---

## 5. Veri Modeli

| Tablo | Açıklama |
|-------|----------|
| users | Kullanıcı bilgileri, şifre hash, streak |
| quotes | Motivasyon alıntıları |
| favorites | Kullanıcı-alıntı favori ilişkisi |
| goals | Kullanıcı hedefleri ve ilerleme |
| notes | Kişisel günlük notları |
| notifications | Bildirim geçmişi |
| badges | Rozet tanımları |
| user_badges | Kullanıcı-rozet kazanım ilişkisi |
