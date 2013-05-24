from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from roster import app
from roster.models import db, Entry, Category
from roster.forms import EntryForm


@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_welcome.html', entries=entries)

def build_race_list():
    racers = Entry.query.filter(Entry.time==None).order_by('id').all()
    nextRaces = []
    while len(racers) > 0 and len(nextRaces) < 6:
        cat = racers[0].categoryId
        nextRace = [ racers.pop(0).name ]
        for i in range(len(racers)):
            if racers[i].categoryId == cat:
                nextRace.append(racers.pop(i).name)
                break
        if len(nextRace) == 1:
            nextRace.append("Anyone!")
        nextRaces.append(nextRace)
    return nextRaces

@app.route('/race')
def show_race():
    entries = Entry.query.order_by('name').all()
    nextRaces = build_race_list()
    return render_template('show_race.html', entries=entries, nextRaces=nextRaces)

@app.route('/roster')
def show_roster():
    racers = Entry.query.filter(Entry.time==None).order_by('id').all()
    entries = Entry.query.order_by('name').all()
    categories = Category.query.all()
    form = EntryForm()
    return render_template('show_roster.html', entries=entries, categories=categories, form=form, racers=racers)

@app.route('/results')
def show_results():
    nextRaces = build_race_list()
    requested_category = int(request.args.get('category',0))
    if requested_category == 0:
        entries = Entry.query.filter(Entry.time != None).order_by(Entry.time).all()
    else:
        entries = Entry.query.filter(Entry.categoryId == requested_category).filter(Entry.time != None).order_by(Entry.time).all()
    if requested_category == 0:
        catname = 'All Categories'
    else:
        catname = Category.query.filter_by(id=requested_category).first().name
    return render_template('show_results.html', entries=entries, catname=catname, next_category=(requested_category+1)% 4, nextRaces=nextRaces)

@app.route('/add_rider', methods=['POST'])
def add_rider():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(form.name)
        form.populate_obj(entry)
        db.session.add(entry)
        try:
            db.session.commit()
            flash('New entry was successfully posted')  
        except:
            flash('Commit failed - name already used?')
        
    return redirect(url_for('show_roster'))

@app.route('/rider/<id>/edit', methods=['GET', 'POST'])
def edit_rider(id):
    rider = Entry.query.get_or_404(id)
    form = EntryForm(obj=rider)
    
    if form.validate_on_submit():
        if 'delete' in request.form:
            db.session.delete(rider)
            flash('Rider was successfully deleted')
            db.session.commit()
        else:
            form.populate_obj(rider)
            try:
                db.session.commit()
            except:
                flash('Update failed - db error?')
                return redirect(url_for('edit_rider', id=id))
            flash('Rider was successfully updated')    
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
        row.history = str(time);
    else:
        row.history = str(row.history) + ', ' + str(time)
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
