from .base_model import BaseModel

# Motivasyon alıntısı sınıfı - BaseModel'den türüyor (kalıtım)
class Quote(BaseModel):
    def __init__(self, id=None, text=None, author=None, category=None, created_at=None):
        super().__init__(id, created_at)
        self.text = text
        self.author = author
        self.category = category

    def __str__(self):
        return f'"{self.text}" - {self.author}'

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'text': self.text,
            'author': self.author,
            'category': self.category
        })
        return base
