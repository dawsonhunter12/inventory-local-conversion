# models.py
from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    part_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    part_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    origin_partnumber = db.Column(db.String(100))
    mcmaster_carr_partnumber = db.Column(db.String(100))
    cost = db.Column(db.Float)
    quantity = db.Column(db.Integer, nullable=False)
    min_on_hand = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
