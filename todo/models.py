from flask_login import UserMixin
from todo import db
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    profile_pic = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    tasks = db.relationship('Task', backref = 'author')
        

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    description = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))