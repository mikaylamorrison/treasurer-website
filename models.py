from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    displayName = db.Column(db.String, default = username, nullable = False)
    streak = db.Column(db.Integer, default = 0, nullable = False)
    sessionsUnpaid = db.Column(db.Integer, default = 0, nullable = False)
    
    def __repr__(self):
        return '<User %r>' % self.username
