import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-super-secret-key")

    # Prefer DATABASE_URL from Render env, fallback to manual Postgres connection
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://parkease_data_user:wE23Fbe1QWSzBPSU2GSLeMFyXgZdXapa@dpg-d2vt87idbo4c73b1id1g-a.oregon-postgres.render.com/parkease_data"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
