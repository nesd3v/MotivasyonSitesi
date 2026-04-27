from .base_model import BaseModel

# Günlük notu sınıfı - BaseModel'den türüyor (kalıtım)
class Note(BaseModel):
    def __init__(self, id=None, user_id=None, title=None, content=None,
                 mood=None, created_at=None):
        super().__init__(id, created_at)
        self.user_id = user_id
        self.title = title
        self.content = content
        self.mood = mood  # happy, motivated, neutral, tired, sad

    # İçeriğin kısa önizlemesini döndürüyorum
    def get_preview(self, length=120):
        if self.content and len(self.content) > length:
            return self.content[:length] + '...'
        return self.content or ''

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'mood': self.mood,
            'preview': self.get_preview()
        })
        return base
