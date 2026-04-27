from flask import Flask
from src.core.config import Config
from src.data.database import init_db, seed_data

# Flask uygulamasını başlatıyorum
# Şablonlar src/ui/ altında, statik dosyalar assets/ altında
app = Flask(__name__, template_folder='src/ui', static_folder='assets')
app.config.from_object(Config)

# Modülleri (Blueprint) kaydet
from src.modules.auth import auth_bp
from src.modules.main import main_bp
from src.modules.quotes import quotes_bp
from src.modules.goals import goals_bp
from src.modules.notes import notes_bp
from src.modules.notifications import notifications_bp
from src.modules.profile import profile_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(quotes_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    init_db()
    seed_data()
    app.run(debug=True)
