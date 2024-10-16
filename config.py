import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Jettson1245')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'inventory_db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
