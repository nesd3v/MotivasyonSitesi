# UML Diyagramları - MotivaSyon Uygulaması

## 1. Use Case Diyagramı

```
+--------------------------------------------------+
|            MotivaSyon Sistemi                    |
|                                                  |
|  +------------------+  +-----------------------+ |
|  | Motivasyon Al    |  | Hedef Ekle/Yönet     | |
|  +------------------+  +-----------------------+ |
|         |                        |               |
|  +------------------+  +-----------------------+ |
|  | Alıntı Favorile  |  | Günlük Not Yaz        | |
|  +------------------+  +-----------------------+ |
|         |                        |               |
|  +------------------+  +-----------------------+ |
|  | Rozet Kazan      |  | Profili Görüntüle     | |
|  +------------------+  +-----------------------+ |
|         |                        |               |
|  +------------------+                           |
|  | Kayıt Ol / Giriş|                            |
|  +------------------+                           |
+--------------------------------------------------+
         |
    [Kullanıcı]  (Tüm use case'lere erişir)
```

---

## 2. Class Diyagramı (OOP Yapısı)

```
+--------------------------------+
|          <<abstract>>          |
|           BaseModel            |
+--------------------------------+
| - id: int                      |
| - created_at: datetime         |
+--------------------------------+
| + to_dict(): dict              |
+--------------------------------+
              /_\
               |
    +----------+----------+----------+----------+
    |          |          |          |          |
    v          v          v          v          v
+--------+ +-------+ +-------+ +------+ +---------+
| User   | | Quote | |  Goal | | Note | |  Badge  |
+--------+ +-------+ +-------+ +------+ +---------+
| -usern | | -text | | -title| | -tit | | -name   |
| -pw_h  | | -auth | | -desc | | -con | | -icon   |
| -email | | -cat  | | -cat  | | -mod | | -cond_t |
| -streak|           | -dead | |      | | -cond_v |
| -login |           | -prog |        |           |
+--------+           | -comp |        |           |
| +upd.. |           +-------+        |           |
| +to_d..|           | +comp()|       |           |
+--------+           | +upd_p()|      | +check_c()|
                     | +overd()|      +-----------+
                     +---------+


+----------------------------------+
|         <<abstract>>             |
|          Notification            |   <-- Polimorfizm
+----------------------------------+      temel sınıfı
| - user_id: int                   |
| - title: str                     |
| - message: str                   |
| - is_read: bool                  |
+----------------------------------+
| + format_message(): str  [abs]   |  <-- Override edilir
| + to_dict(): dict                |
+----------------------------------+
              /_\
               |
    +----------+----------+
    |          |          |
    v          v          v
+----------+ +--------+ +----------+
|Motivational| | Goal  | |  Badge  |  <-- Polimorfizm
|Notification| |Notif. | |  Notif. |      uygulaması
+----------+ +--------+ +----------+
| -category| |-goal_t | |-badge_nm |
+----------+ +--------+ +----------+
| +format()| |+format()| |+format()|  <-- Her biri farklı
|  override| | override| | override|      davranış gösterir
+----------+ +--------+ +----------+
```

### Kullanılan OOP Prensipleri:

| Prensip | Uygulama |
|---------|----------|
| **Kalıtım** | `User`, `Quote`, `Goal`, `Note`, `Badge` → `BaseModel`'den türetiliyor |
| **Kalıtım** | `MotivationalNotification`, `GoalNotification`, `BadgeNotification` → `Notification`'dan türetiliyor |
| **Polimorfizm** | Her bildirim alt sınıfı `format_message()` metodunu farklı şekilde implement ediyor |
| **Kapsülleme** | Veri doğrulama (`update_progress`, `hash_password`) sınıf içinde |
| **Soyutlama** | `Notification.format_message()` abstract metot olarak tanımlanmış |

---

## 3. Sınıf İlişki Özeti

```
User    1 --- * Goal          (Bir kullanıcının çok hedefi var)
User    1 --- * Note          (Bir kullanıcının çok notu var)
User    1 --- * Notification  (Bir kullanıcının çok bildirimi var)
User    * --- * Quote         (Favoriler üzerinden çoka-çok ilişki)
Badge   * --- * User          (user_badges üzerinden çoka-çok ilişki)
```
