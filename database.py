from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    bases = db.relationship('KeyBase', backref='user', lazy=True)

    def __repr__(self):
        return f'User <{self.username}>'

class KeyBase(db.Model):
    __tablename__ = "bases"

    base_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    base_name = db.Column(db.String(100), nullable=False)

    keys = db.relationship('Keys', backref='base', lazy=True)

    def __repr__(self):
        return f'KeyBase <{self.base_name}>'

class Keys(db.Model):
    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('bases.base_id'), nullable=False)
    keyname = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(255), nullable=False) 

    def __repr__(self):
        return f'Key <{self.keyname}>'
