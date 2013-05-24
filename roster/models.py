from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from roster import app

import random

db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False, unique=True)

    age = db.Column(db.Integer)
    club = db.Column(db.String(100))

    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category")

    time = db.Column(db.Float)
    history = db.Column(db.String(100))

    def __init__(self, name, age=None, club=None):
        self.name = name
        self.age = age
        self.club = club


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
    cMen = Category.query.filter_by(name='Men').first()
    for firstname in ['Alan', 'Byron', 'Chad', 'Dave', 'Ed', 'Fred', 'Ginger', 'Harry']:
        for lastname in [' Aardvark', ' Bemer', ' Corney', ' Dilligent', ' Emerson', ' Fitzgerald', ' Gerrard', ' Hopeful']:
            m1 = Entry(firstname + lastname, 21)
            m1.category = cMen
            m1.time = random.uniform(11,22)
            db.session.add(m1)

    cWomen = Category.query.filter_by(name='Women').first()

    for firstname in ['Annie', 'Bonnie', 'Claire', 'Donna', 'Emma']:
        for lastname in [' Aardvark', ' Bemer', ' Corney', ' Dilligent', ' Emerson']:
            m1 = Entry(firstname + lastname, 21)
            m1.category = cWomen
            db.session.add(m1)

    cChild = Category.query.filter_by(name='Under 16').first()

    for firstname in ['Alfie', 'Billy', 'Cedric', 'Danny', 'Ernie']:
        for lastname in [' Aardvark', ' Bemer', ' Corney', ' Dilligent', ' Emerson']:
            m1 = Entry(firstname + lastname, 21)
            m1.category = cChild
            db.session.add(m1)


    db.session.commit()

