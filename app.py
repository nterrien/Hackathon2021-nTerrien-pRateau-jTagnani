from flask import Flask, flash, request, redirect, url_for, make_response, session
from flask_hashing import Hashing
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
from wtforms.validators import DataRequired, EqualTo
import flask  # BSD License (BSD-3-Clause)
import os
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from forms.washing_machine_form import WashingMachineForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import getMachineList, initWashingMachineList, findMachineWith404
from bdd.objects.room import getRoomList, initRoomList, findRoomWith404
from bdd.dbMethods import addUser, findUser, updateUser, updateUsername
from datetime import datetime, date


app = Flask(__name__)
hashing = Hashing(app)
Bootstrap(app)
datepicker(app)
app.config.from_object('config')

db.init_app(app)


def initApp():
    ''' Initialise la base de données et la liste des machines disponibles'''
    init_database()
    initWashingMachineList()
    initRoomList()


with app.app_context():
    initApp()

# Route de base qui conduit à Login si l'utilisateur n'est pas identifié et à home si il l'est
@app.route('/', methods=["GET", "POST"])
def home():
    user = None
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        username = None
        if session.get('username') != None :
            username = session.get('username')
        return flask.render_template("home.html.jinja2", username=username)

# Page de login
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'GET' :
        return flask.render_template("login.html.jinja2") 
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Bon id/mdp ?
        result = request.form
        username = result['username']
        if findUser(username) == None :
            flash('wrong username')
            return flask.render_template("login.html.jinja2")
        user = findUser(username)
        hashPassword = user.password
        passw = result['password']   
        if hashing.check_value(hashPassword, passw, salt='abcd'): 
            session['username'] = username
            session['logged_in'] = True
        else:
            flash('wrong password!') 
        return redirect(url_for('home'))
   
           
    #return home()

# logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    #return home()
    return redirect(url_for('home'))

# signin
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #Ajout des données dans la bdd
        result = request.form
        username = result['username']
        password = result['password']
        
        # Pour l'instant en clair mais à améliorer : hashage
        hashPassword = hashing.hash_value(password, salt='abcd')
        if findUser(username) == None :
            addUser(username, hashPassword)
            print(hashPassword)
            session['logged_in'] = True
        else :
            flash('Oups ! Sign in failed, user already exists')
        session['username'] = username    
        return redirect(url_for('do_admin_login'))
    return flask.render_template("signin.html.jinja2")


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])

class ChangePassword(Form):
    password = PasswordField('New Password', [validators.DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat password')

class UsernameForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    

@app.route('/changePassword', methods=["GET", "POST"])
def change():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    form = ChangePassword(request.form)
    result=request.form
    if request.method == 'POST':
        if form.validate() : 
            result=request.form
            username = session.get('username')
            print(username)
            user = findUser(username)
            if hashing.check_value(user.password, result['oldPassword'], salt='abcd'):
                password = result['password']
                hashPassword = hashing.hash_value(password, salt='abcd')
                updateUser (user, username, hashPassword)
                return flask.render_template("home.html.jinja2")
        else :
            flash('Issue')    
    return flask.render_template('changePassword.html.jinja2')

@app.route('/profil', methods=["GET", "POST"])
def profil():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    form = UsernameForm(request.form)
    if request.method == 'POST' and form.validate():
        result=request.form
        username = session.get('username')
        user = findUser(username)
        updateUsername(user, result['username'])
        user = result['username']
        session['username'] = user
        return redirect(url_for('profil'))
    if 'username' in session :
        username = None
        username = session.get('username')
        return flask.render_template('profil.html.jinja2', username=username)    


@app.route('/general', methods=["GET", "POST"])
def general():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        return flask.render_template("general.html.jinja2")
    


@app.route('/washing', methods=["GET", "POST"])
def washing():
    if session.get('logged_in'):
        form = WashingMachineForm(obj=getMachineList())
        form.agenda.machine.choices = [g.index for g in getMachineList()]
        if "reservation" in request.form and form.reservation.validate(form):
            machine = findMachineWith404(form.agenda.machine.data)
            datetimeStart = datetime.combine(
                form.reservation.startDate.data, form.reservation.startHour.data)
            success = machine.reserve(datetimeStart)
            if success == False:
                flash("Le créneau " + str(form.reservation.startHour.data.strftime('%H:%M')) +
                      ' - ' + str((datetimeStart + machine.duration).time().strftime('%H:%M')) + " de la machine " + str(form.agenda.machine.data) + " est déjà pris.", "warning")
            else:
                flash("Le créneau a bien été reservé.", "success", )
            form.agenda.date.data = form.reservation.startDate.data
            return flask.render_template("washing.html.jinja2", form=form, week=getDayWeek(form.reservation.startDate.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findMachineWith404(form.agenda.machine.data)))
        elif "agenda" in request.form and form.agenda.validate(form):
            form.reservation.startDate.data = form.agenda.date.data
            return flask.render_template("washing.html.jinja2", form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findMachineWith404(form.agenda.machine.data)))
        else:
            form.agenda.machine.data = getMachineList()[0].index
            form.agenda.date.data = date.today()
            form.reservation.startDate.data = form.agenda.date.data
            return flask.render_template("washing.html.jinja2", form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findMachineWith404(form.agenda.machine.data)))
    else :
        return redirect(url_for('home'))        


def getDayWeek(day):
    weekday = day.isoweekday()
    start = day - timedelta(days=weekday-1)
    dates = [start + timedelta(days=d) for d in range(7)]
    return dates

# Les donner retourner sont une liste avec chaque element qui correspond à un jour de la semaine
# Chaque jour est une liste de reservations composé de le % de la journée que represente cette reservation, le nom du reservant, l'heure de debut, l'heure de fin.
# Si None est le nom du reservant cela signifie que c'est une reservation vide utilisé pour faire des trous dans l'afficahge en HTML


def getReservationWeek(week, machine):
    agenda = []
    for day in week:
        reservations = machine.checkDate(day)
        dayAgenda = []
        for reservation in reservations:
            dayAgenda.append([100*((timeToMinutes(reservation.end)-timeToMinutes(reservation.start))/(24*60)),
                              reservation.name, reservation.start.time(), reservation.end.time()])
        current = 0
        schedule = []
        for reservation in dayAgenda:
            if (reservation[0] != current):
                schedule.append(
                    [100*(timeToMinutes(reservation[2]) - current)/(24*60), None, None, None])
            schedule.append(reservation)
            current = timeToMinutes(reservation[3])
        agenda.append(schedule)
    return agenda


def timeToMinutes(time):
    return time.hour*60+time.minute


@app.route('/reset', methods=["GET", "POST"])
def reset():
    ''' Sur ce endpoint, on reset la base de données'''
    clear_database()
    initApp()
    return flask.render_template("home.html.jinja2")

# Pages pour montrer le fonctionnement de WashingMachine


@app.route('/machine/findAll', methods=["GET", "POST"])
def findAllMachines():
    print (getMachineList())
    return flask.render_template("home.html.jinja2")


@app.route('/machine/<id>/check', methods=["GET", "POST"])
def check(id):
    machine = findMachineWith404(id)
    print(machine.checkDate(date.today()))
    return flask.render_template("home.html.jinja2")


''' Accède à la machine id et regarde les réservations de tous les temps '''


@app.route('/machine/<id>/findAll', methods=["GET", "POST"])
def findAllReservations(id):
    machine = findMachineWith404(id)
    print(machine.findAll())
    return flask.render_template("home.html.jinja2")


@app.route('/machine/<id>/reserve', methods=["GET", "POST"])
def reserve(id):
    machine = findMachineWith404(id)
    machine.reserve(datetime.today())
    return flask.render_template("home.html.jinja2")

# Pages pour montrer le fonctionnement de User


@app.route('/user/create', methods=["GET", "POST"])
def create():
    addUser("admin", "password")
    return flask.render_template("home.html.jinja2")


@app.route('/user/find', methods=["GET", "POST"])
def find():
    print(findUser("admin"))
    return flask.render_template("home.html.jinja2")


@app.route('/user/update', methods=["GET", "POST"])
def update():
    user = findUser("admin")
    updateUser(user, "admin2", "new password")
    return flask.render_template("home.html.jinja2")


@ app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
