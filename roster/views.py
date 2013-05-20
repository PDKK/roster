from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from roster import app
from roster.models import db, Entry, Category
from roster.forms import EntryForm


@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_welcome.html', entries=entries)

@app.route('/race')
def show_race():
    entries = Entry.query.all()
    return render_template('show_race.html', entries=entries)

@app.route('/roster')
def show_roster():
    entries = Entry.query.all()
    categories = Category.query.all()
    form = EntryForm()
    return render_template('show_roster.html', entries=entries, categories=categories, form=form)

@app.route('/results')
def show_results():
    requested_category = int(request.args.get('category',0))
    if requested_category == 0:
        entries = Entry.query.filter(Entry.time != None).order_by(Entry.time).all()
    else:
        entries = Entry.query.filter(Entry.categoryId == requested_category).filter(Entry.time != None).order_by(Entry.time).all()
    if requested_category == 0:
        catname = 'All Categories'
    else:
        catname = Category.query.filter_by(id=requested_category).first().name
    return render_template('show_results.html', entries=entries, catname=catname, next_category=(requested_category+1)% 4)

@app.route('/add_rider', methods=['POST'])
def add_rider():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(form.name)
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        flash('New entry was successfully posted')    
    return redirect(url_for('show_roster'))

@app.route('/rider/<id>/edit', methods=['GET', 'POST'])
def edit_rider(id):
    rider = Entry.query.get_or_404(id)
    form = EntryForm(obj=rider)
    if form.validate_on_submit():
        form.populate_obj(rider)
        db.session.commit()
        flash('Rider was successfully posted')    
        return redirect(url_for('show_roster'))
    else:    
        # Get the data from the database
        return render_template('edit_rider.html', form=form, id=id)




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
    row = Entry.query.get_or_404(id)
    if row.history == None:
        history = str(time);
    else:
        history = str(row.history) + ', ' + str(time)
    if row.time == None or float(time) < row.time:
        row.time = float(time)
    db.session.commit()


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
