# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'roster.db'
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
    requested_category = int(request.args.get('category',0))
    if requested_category == 0:
        cur = g.db.execute('select entries.name, category, time, categories.name from entries inner join categories on entries.category = categories.id where time NOT NULL order by time asc ')
    else:
        cur = g.db.execute('select entries.name, category, time, categories.name from entries inner join categories on entries.category = categories.id where time NOT NULL and entries.category = ? order by category asc, time asc ', [requested_category])
    entries = [dict(name=row[0], category=row[1], time=row[2], catname=row[3]) for row in cur.fetchall()]
    if requested_category == 0:
        catname = 'All Categories'
    else:
        cur = g.db.execute('select name from categories where id = ?', [requested_category])
        row = cur.fetchone()
        catname = row[0]
    return render_template('show_results.html', entries=entries, catname=catname, next_category=(requested_category+1)% 4)

@app.route('/add_rider', methods=['POST'])
def add_rider():
    g.db.execute('insert into entries (name, age, club, category) values (?, ?, ?, ?)',
                 [request.form['name'], request.form['age'],request.form['club'],request.form['category']])
    g.db.commit()
    flash('New entry was successfully posted')    
    return redirect(url_for('show_roster'))

@app.route('/rider/<id>/edit', methods=['GET', 'POST'])
def edit_rider(id):
    if request.method == 'GET':
        # Get the data from the database
        cur = g.db.execute('select id,name from categories order by id asc')
        categories = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
        cur = g.db.execute('select name, age, club, category, time, history from entries where id=?', [id])
        row = cur.fetchone()
        return render_template('edit_rider.html',
                               id=id,
                               name=row[0],
                               age=row[1],
                               club=row[2],
                               category=row[3],
                               time = row[4],
                               history = row[5],
                               categories = categories);
    else:
        # Update the details
        g.db.execute('update entries set name=?, age=?, club=?, category=?, time=?, history=? where id = ?',
                     [request.form['name'], 
                      request.form['age'], 
                      request.form['club'], 
                      request.form['category'],
                      request.form['time'],
                      request.form['history'],
                      id])
        g.db.commit()
        flash('Rider was successfully posted')    
        return redirect(url_for('show_roster'))



@app.route('/add_result', methods=['POST'])
def add_result():
    try:
        float(request.form['bluetime'])
        float(request.form['redtime'])
    except:
        flash("Put a time in, you numpty")
        return redirect(url_for('show_race'))
    add_one_result(request.form['blueid'], request.form['bluetime'])
    add_one_result(request.form['redid'], request.form['redtime'])
    return redirect(url_for('show_race'))

def add_one_result(id, time):        
    cur = g.db.execute('select time, history from entries where id = ?', [id])
    row = cur.fetchone()
    if row[1] == None:
        history = str(time);
    else:
        history = str(row[1]) + ', ' + str(time)
    if row[0] == None or float(time) < row[0]:
        g.db.execute('update entries set time = ?, history = ? where id = ?', [time, history, id])
        g.db.commit()
    else:
        g.db.execute('update entries set history = ? where id = ?', [history, id])
        g.db.commit()


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


