import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-super-secret-key")

    # Prefer DATABASE_URL from Render env, fallback to your manual Postgres connection
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or
        "postgresql://parkease_data_user:wE23Fbe1QWSzBPSU2GSLeMFyXgZdXapa@dpg-d2vt87idbo4c73b1id1g-a.oregon-postgres.render.com/parkease_data"
