from .base_model import BaseModel
from datetime import datetime

# Hedef sınıfı - BaseModel'den türüyor (kalıtım)
class Goal(BaseModel):
    def __init__(self, id=None, user_id=None, title=None, description=None,
                 category=None, deadline=None, is_completed=False, progress=0, created_at=None):
        super().__init__(id, created_at)
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.deadline = deadline
        self.is_completed = is_completed
        self.progress = progress

    # Hedefi tamamlandı olarak işaretliyorum
    def complete(self):
        self.is_completed = True
        self.progress = 100

    # İlerlemeyi 0-100 arasında güncelliyorum
    def update_progress(self, value):
        self.progress = max(0, min(100, int(value)))
        if self.progress == 100:
            self.is_completed = True

    # Süre doldu mu kontrolü
    def is_overdue(self):
        if self.deadline and not self.is_completed:
            try:
                deadline_dt = datetime.fromisoformat(str(self.deadline))
                return datetime.now() > deadline_dt
            except:
                return False
        return False

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'deadline': str(self.deadline) if self.deadline else None,
            'is_completed': self.is_completed,
            'progress': self.progress
        })
        return base
