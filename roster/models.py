from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from roster import app

db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)

    age = db.Column(db.Integer)
    club = db.Column(db.String(100))

    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category")

    time = db.Column(db.Float)
    history = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return '<Entry name:%r>' % self.name

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name


def init_db():
    db.create_all()
    m = Category('Men')
    m.id = 1
    w = Category('Women')
    w.id = 2
    u = Category('Under 16')
    u.id = 3
    db.session.add(m)
    db.session.add(w)
    db.session.add(u)
    db.session.commit()

def add_test_data():
    db.session.commit()

