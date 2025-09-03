import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///parking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123') 

