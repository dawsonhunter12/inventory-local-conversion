import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Jettson1245!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        os.environ.get('DB_USER', 'user'),
        os.environ.get('DB_PASSWORD', 'password'),
        os.environ.get('DB_HOST', 'db'),
        os.environ.get('DB_NAME', 'inventory_db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
