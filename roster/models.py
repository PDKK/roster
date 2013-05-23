from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from roster import app

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
    m1 = Entry('Alf Aardvark', 21, 'Aardmans')
    m1.category = cMen
    db.session.add(m1)
    m2 = Entry('Bob Bemer', 22, 'Aardmans')
    m2.category = cMen
    db.session.add(m2)
    m3 = Entry('Charles Corney', 23, 'Aardmans')
    m3.category = cMen
    db.session.add(m3)
    m4 = Entry('David Dilligent', 24, 'Aardmans')
    m4.category = cMen
    db.session.add(m4)
    m5 = Entry('Ed Emeriay', 25, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)
    m5 = Entry('Fred Fotheringay', 26, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)
    m5 = Entry('Greg Gemeriay', 21, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)
    m5 = Entry('Harry Hemeriay', 21, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)
    m5 = Entry('Ian Imeriay', 21, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)
    m5 = Entry('Jack Jemeriay', 21, 'Aardmans')
    m5.category = cMen
    db.session.add(m5)

    cWomen = Category.query.filter_by(name='Women').first()
    m1 = Entry('WAlf Aardvark', 21, 'Aardmans')
    m1.category = cWomen
    db.session.add(m1)
    m2 = Entry('WBob Bemer', 22, 'Aardmans')
    m2.category = cWomen
    db.session.add(m2)
    m3 = Entry('WCharles Corney', 23, 'Aardmans')
    m3.category = cWomen
    db.session.add(m3)
    m4 = Entry('WDavid Dilligent', 24, 'Aardmans')
    m4.category = cWomen
    db.session.add(m4)
    m5 = Entry('WEd Emeriay', 25, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)
    m5 = Entry('WFred Fotheringay', 26, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)
    m5 = Entry('WGreg Gemeriay', 21, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)
    m5 = Entry('WHarry Hemeriay', 21, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)
    m5 = Entry('WIan Imeriay', 21, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)
    m5 = Entry('WJack Jemeriay', 21, 'Aardmans')
    m5.category = cWomen
    db.session.add(m5)

    cChild = Category.query.filter_by(name='Under 16').first()
    m1 = Entry('CAlf Aardvark', 21, 'Aardmans')
    m1.category = cChild
    db.session.add(m1)
    m2 = Entry('CBob Bemer', 22, 'Aardmans')
    m2.category = cChild
    db.session.add(m2)
    m3 = Entry('CCharles Corney', 23, 'Aardmans')
    m3.category = cChild
    db.session.add(m3)
    m4 = Entry('CDavid Dilligent', 24, 'Aardmans')
    m4.category = cChild
    db.session.add(m4)
    m5 = Entry('CEd Emeriay', 25, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)
    m5 = Entry('CFred Fotheringay', 26, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)
    m5 = Entry('CGreg Gemeriay', 21, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)
    m5 = Entry('CHarry Hemeriay', 21, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)
    m5 = Entry('CIan Imeriay', 21, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)
    m5 = Entry('CJack Jemeriay', 21, 'Aardmans')
    m5.category = cChild
    db.session.add(m5)


    db.session.commit()

