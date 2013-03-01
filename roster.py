# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/roster.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select name, age from entries order by id desc')
    entries = [dict(name=row[0], sex=row[1]) for row in cur.fetchall()]
    return render_template('show_welcome.html', entries=entries)

@app.route('/race')
def show_race():
    cur = g.db.execute('select id, name, age from entries order by id asc')
    entries = [dict(id=row[0], name=row[1], age=row[2]) for row in cur.fetchall()]
    return render_template('show_race.html', entries=entries)

@app.route('/roster')
def show_roster():
    cur = g.db.execute('select id, name, age, category, club from entries order by id asc')
    entries = [dict(id=row[0], name=row[1], age=row[2], category=row[3], club=row[4]) for row in cur.fetchall()]
    cur = g.db.execute('select id,name from categories order by id asc')
    categories = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

    return render_template('show_roster.html', entries=entries, categories=categories)

@app.route('/results')
def show_results():
    cur = g.db.execute('select name, category, time from entries where time NOT NULL order by category asc, time asc ')
    entries = [dict(name=row[0], category=row[1], time=row[2]) for row in cur.fetchall()]
    cur = g.db.execute('select id,name from categories order by id asc')
    categories = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return render_template('show_results.html', entries=entries, categories=categories)

@app.route('/add_rider', methods=['POST'])
def add_rider():
    g.db.execute('insert into entries (name, age, club, category) values (?, ?, ?, ?)',
                 [request.form['name'], request.form['age'],request.form['club'],request.form['category']])
    g.db.commit()
    flash('New entry was successfully posted')    
    return redirect(url_for('show_roster'))

@app.route('/add_result', methods=['POST'])
def add_result():
    try:
        float(request.form['bluetime'])
        float(request.form['redtime'])
    except:
        flash("Put a time in, you numpty")
        return redirect(url_for('show_race'))
        
    cur = g.db.execute('select time from entries where id = ?', [request.form['blueid']])
    row = cur.fetchone()
    if row[0] == None or float(request.form['bluetime']) < row[0]:
        g.db.execute('update entries set time = ? where id = ?', [request.form['bluetime'], request.form['blueid']])
        g.db.commit()
    cur = g.db.execute('select time from entries where id = ?', [request.form['redid']])
    row = cur.fetchone()
    if row[0] == None or float(request.form['redtime']) < row[0]:
        g.db.execute('update entries set time = ? where id = ?', [request.form['redtime'], request.form['redid']])
        g.db.commit()
    return redirect(url_for('show_race'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')


