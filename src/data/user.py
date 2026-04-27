from .base_model import BaseModel
from datetime import datetime

# Kullanıcı sınıfı - BaseModel'den türüyor (kalıtım)
class User(BaseModel):
    def __init__(self, id=None, username=None, password_hash=None,
                 email=None, streak=0, last_login=None, created_at=None):
        super().__init__(id, created_at)
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.streak = streak
        self.last_login = last_login

    # Günlük giriş serisini hesaplayıp güncelliyorum
    def update_streak(self):
        today = datetime.now().date()
        if self.last_login:
            try:
                if isinstance(self.last_login, str):
                    last = datetime.fromisoformat(self.last_login).date()
                else:
                    last = self.last_login.date()
                fark = (today - last).days
                if fark == 1:
                    self.streak += 1
                elif fark > 1:
                    self.streak = 1
                # Aynı gün giriş yapıldıysa seri değişmez
            except:
                self.streak = 1
        else:
            self.streak = 1
        self.last_login = datetime.now()
        return self.streak

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'username': self.username,
            'email': self.email,
            'streak': self.streak,
            'last_login': str(self.last_login) if self.last_login else None
        })
        return base
