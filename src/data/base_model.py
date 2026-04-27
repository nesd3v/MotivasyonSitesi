from datetime import datetime

# Tüm modellerin türeyeceği temel sınıf
class BaseModel:
    def __init__(self, id=None, created_at=None):
        self.id = id
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': str(self.created_at)
        }
