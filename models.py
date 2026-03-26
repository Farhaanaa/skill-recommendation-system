from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    profiles      = db.relationship("UserProfile", backref="user", lazy=True)
    bookmarks     = db.relationship("Bookmark", backref="user", lazy=True)


class UserProfile(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    interests     = db.Column(db.Text)
    qualification = db.Column(db.String(100))
    course        = db.Column(db.String(100))
    career        = db.Column(db.String(100))
    career_goal   = db.Column(db.String(100))
    skills        = db.Column(db.Text)
    certifications= db.Column(db.Text)
    tools_known   = db.Column(db.Text)
    what_they_know= db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)


class Bookmark(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    project_domain= db.Column(db.String(100))
    saved_at      = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    liked         = db.Column(db.Boolean, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)