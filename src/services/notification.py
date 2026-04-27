from src.data.base_model import BaseModel

# Temel bildirim sınıfı - polimorfizm için
class Notification(BaseModel):
    def __init__(self, id=None, user_id=None, title=None, message=None,
                 is_read=False, created_at=None):
        super().__init__(id, created_at)
        self.user_id = user_id
        self.title = title
        self.message = message
        self.is_read = is_read

    # Alt sınıflar bu metodu kendi şekilde yazacak (polimorfizm)
    def format_message(self):
        raise NotImplementedError("Alt sınıflarda tanımlanmalı")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read
        })
        return base


# Motivasyon bildirimi - Notification'dan kalıtım alıyor
class MotivasyonBildirimi(Notification):
    def __init__(self, kategori=None, **kwargs):
        super().__init__(**kwargs)
        self.kategori = kategori

    def format_message(self):
        return f"[Motivasyon - {self.kategori}] {self.message}"


# Hedef tamamlama bildirimi
class HedefBildirimi(Notification):
    def __init__(self, hedef_adi=None, **kwargs):
        super().__init__(**kwargs)
        self.hedef_adi = hedef_adi

    def format_message(self):
        return f"[Hedef Tamamlandı] {self.hedef_adi}: {self.message}"


# Rozet kazanma bildirimi
class RozetBildirimi(Notification):
    def __init__(self, rozet_adi=None, **kwargs):
        super().__init__(**kwargs)
        self.rozet_adi = rozet_adi

    def format_message(self):
        return f"[Yeni Rozet: {self.rozet_adi}] {self.message}"
