# MotivaSyon - Web Tabanlı Dinamik Motivasyon Bildirim Sistemi

## Proje Açıklaması
MotivaSyon, kullanıcıların günlük motivasyonunu yüksek tutmasına yardımcı olan, web tabanlı dinamik bir uygulamadır. Tek bir butona basarak anında motivasyon bildirimi alabilir, hedeflerinizi takip edebilir, kişisel günlüğünüzü tutabilir ve başarı rozetleri kazanabilirsiniz.

## Özellikler
1. **Motivasyon Bildirimi** - Rastgele alıntılarla anlık motivasyon, tarayıcı push bildirimi desteği
2. **Hedef Takip Sistemi** - Hedef ekleme, ilerleme takibi, kategori ve bitiş tarihi
3. **Alıntı Koleksiyonu** - 25+ motivasyon alıntısı, kategori filtresi, favorilere ekleme
4. **Kişisel Günlük** - Ruh hali destekli not yazma, detay modal görünümü
5. **Başarı Rozet Sistemi** - Aktiviteye dayalı otomatik rozet kazanımı
6. **Kullanıcı Profili** - İstatistikler, günlük seri, bildirim geçmişi

## Kullanılan Teknolojiler
| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.x, Flask 3.0 |
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| UI Framework | Bootstrap 5.3 |
| Veritabanı | SQLite |
| OOP | Kalıtım + Polimorfizm (Python) |

## OOP Yapısı
- **Kalıtım:** `User`, `Quote`, `Goal`, `Note`, `Badge` → `BaseModel`
- **Polimorfizm:** `MotivationalNotification`, `GoalNotification`, `BadgeNotification` → `Notification.format_message()` override

## Klasör Yapısı
```
MotivasyonSitesi/
├── docs/                    # Dokümanlar
│   ├── GereksinimAnalizi.md
│   └── UML_Diyagramlari.md
├── src/
│   ├── models/              # OOP model sınıfları
│   ├── routes/              # Flask Blueprint route'ları
│   └── utils/               # Yardımcı fonksiyonlar
├── templates/               # Jinja2 HTML şablonları
├── static/
│   ├── css/style.css
│   └── js/
├── tests/test_models.py     # Birim testleri
├── app.py                   # Uygulama giriş noktası
├── config.py                # Yapılandırma
└── requirements.txt
```

## Kurulum ve Çalıştırma
```bash
# Gerekli paketleri yükle
pip install -r requirements.txt

# Uygulamayı başlat (veritabanı ve örnek veriler otomatik oluşturulur)
python app.py
```
Tarayıcıda `http://localhost:5000` adresini aç.

## Testleri Çalıştırma
```bash
python tests/test_models.py
```

## Geliştirici
Proje sahibi: Enes Çelik  
E-posta: celikenes984@gmail.com  
Tarih: Nisan 2026
