from flask import Flask, render_template
from models import db
from flask_login import LoginManager
from config import Config

from admin import admin_bp
from auth import auth_bp
from user import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from datetime import datetime, timedelta

    @app.context_processor
    def inject_datetime():
        return dict(datetime=datetime, timedelta=timedelta)

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.route('/')
    def home():
        return render_template('hero.html')

    # ✅ Ensure tables exist (for Render too)
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
