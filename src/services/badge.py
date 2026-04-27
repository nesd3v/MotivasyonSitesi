from src.data.base_model import BaseModel

# Rozet sınıfı - koşul kontrolü yapıyor
class Badge(BaseModel):
    def __init__(self, id=None, name=None, description=None, icon=None,
                 condition_type=None, condition_value=None, created_at=None):
        super().__init__(id, created_at)
        self.name = name
        self.description = description
        self.icon = icon
        self.condition_type = condition_type  # streak, goals_completed, notes_count, favorites_count
        self.condition_value = condition_value

    # Kullanıcı bu rozeti kazandı mı kontrol ediyorum
    def check_condition(self, user_stats):
        deger = user_stats.get(self.condition_type, 0)
        return deger >= self.condition_value

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'condition_type': self.condition_type,
            'condition_value': self.condition_value
        })
        return base
