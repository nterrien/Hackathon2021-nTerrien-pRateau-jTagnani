from flask import Flask, flash, request, redirect, url_for, make_response, session
from flask_hashing import Hashing
import flask  # BSD License (BSD-3-Clause)
import os
from datetime import datetime, date, timedelta
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from forms.washing_machine_form import WashingMachineForm
from forms.room_form import RoomForm
from forms.login_forms import RegistrationForm, ChangePassword, UsernameForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.dbMethods import addUser, findUser, updateUser, updateUsername
from utils.objects.washingMachine import getMachineList, initWashingMachineList, findMachineWith404
from utils.objects.room import getRoomList, initRoomList, findRoomWith404


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
        if session.get('username') != None:
            username = session.get('username')
        return flask.render_template("home.html.jinja2", username=username)

# Page de login
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'GET':
        return flask.render_template("login.html.jinja2")
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Bon id/mdp ?
        result = request.form
        username = result['username']
        if findUser(username) == None:
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
    return flask.render_template("login.html.jinja2")

# logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    # return home()
    return redirect(url_for('home'))

# signin
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Ajout des données dans la bdd
        result = request.form
        username = result['username']
        password = result['password']

        # Pour l'instant en clair mais à améliorer : hashage
        hashPassword = hashing.hash_value(password, salt='abcd')
        if findUser(username) == None:
            addUser(username, hashPassword)
            print(hashPassword)
        else:
            flash('Oups ! Sign in failed, user already exists')
        session['username'] = username
        return redirect(url_for('do_admin_login'))
    return flask.render_template("signin.html.jinja2")


@app.route('/changePassword', methods=["GET", "POST"])
def change():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    form = ChangePassword(request.form)
    result = request.form
    if request.method == 'POST':
        if form.validate():
            result = request.form
            username = session.get('username')
            print(username)
            user = findUser(username)
            if hashing.check_value(user.password, result['oldPassword'], salt='abcd'):
                password = result['password']
                hashPassword = hashing.hash_value(password, salt='abcd')
                updateUser(user, username, hashPassword)
                return flask.render_template("home.html.jinja2")
        else:
            flash('Issue')
    return flask.render_template('changePassword.html.jinja2')


@app.route('/profil', methods=["GET", "POST"])
def profil():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    form = UsernameForm(request.form)
    if request.method == 'POST' and form.validate():
        result = request.form
        username = session.get('username')
        user = findUser(username)
        updateUsername(user, result['username'])
        user = result['username']
        session['username'] = user
        return redirect(url_for('profil'))
    if 'username' in session:
        username = None
        username = session.get('username')
        return flask.render_template('profil.html.jinja2', username=username)


@app.route('/general', methods=["GET", "POST"])
def general():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        return flask.render_template("general.html.jinja2")


# Page de reservation des machines à laver
@app.route('/washing', methods=["GET", "POST"])
def washing():
    def reserve_washingmachine(form):
        machine = findMachineWith404(form.agenda.reservable.data)
        datetimeStart = datetime.combine(
            form.reservation.startDate.data, form.reservation.startHour.data)
        success = machine.reserve(datetimeStart, session['username'])
        if success == False:
            flash("Le créneau " + str(form.reservation.startHour.data.strftime('%H:%M')) +
                  ' - ' + str((datetimeStart + machine.duration).time().strftime('%H:%M')) + " du " + str(form.reservation.startDate.data.strftime('%d/%m/%Y')) + " de la machine " + str(form.agenda.reservable.data) + " est déjà pris.", "warning")
        else:
            flash("Le créneau a bien été reservé.", "success")

    return reservation_general(getMachineList, findMachineWith404, reserve_washingmachine,
                               "machine", "washing.html.jinja2")

# Page de reservation des salles
@app.route('/room', methods=["GET", "POST"])
def room():
    def reserve_room(form):
        reservable = findRoomWith404(
            form.agenda.reservable.data)
        duration = timedelta(minutes=form.reservation.duration.data)
        datetimeStart = datetime.combine(
            form.reservation.startDate.data, form.reservation.startHour.data)
        success = reservable.reserve(
            datetimeStart, duration, session['username'])
        if success == False:
            flash("Le créneau " + str(form.reservation.startHour.data.strftime('%H:%M')) +
                  ' - ' + str((datetimeStart + duration).time().strftime('%H:%M')) + " du " + str(form.reservation.startDate.data.strftime('%d/%m/%Y')) + " de la salle " + str(form.agenda.reservable.data) + " est déjà pris.", "warning")
        else:
            flash("Le créneau a bien été reservé.", "success")

    return reservation_general(getRoomList, findRoomWith404, reserve_room,
                               "salle", "room.html.jinja2")


def reservation_general(reservableListMethods, findReservablewith404, reservationMethod, reservable_type, template_name):
    if session.get('logged_in'):
        form = RoomForm(obj=reservableListMethods())
        form.agenda.reservable.choices = [
            g.index for g in reservableListMethods()]
        if "reservation" in request.form and form.reservation.validate(form):
            success = reservationMethod(form)
            form.agenda.date.data = form.reservation.startDate.data
            return flask.render_template(template_name, form=form, week=getDayWeek(form.reservation.startDate.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=session['username'], reservable_type=reservable_type)
        elif "agenda" in request.form and form.agenda.validate(form):
            form.reservation.startDate.data = form.agenda.date.data
            return flask.render_template(template_name, form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=session['username'], reservable_type=reservable_type)
        else:
            form.agenda.reservable.data = reservableListMethods()[0].index
            form.agenda.date.data = date.today()
            form.reservation.startDate.data = form.agenda.date.data
            return flask.render_template(template_name, form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=session['username'], reservable_type=reservable_type)
    else:
        return redirect(url_for('home'))


def getDayWeek(day):
    weekday = day.isoweekday()
    start = day - timedelta(days=weekday-1)
    dates = [start + timedelta(days=d) for d in range(7)]
    return dates


def getReservationWeek(week, reservable):
    '''Les données retournées sont une liste avec chaque element qui correspond à un jour de la semaine
    Chaque jour est une liste de reservations composé de le % de la journée que represente cette reservation, le nom du reservant, l'heure de debut, l'heure de fin.
    Si None est le nom du reservant cela signifie que c'est une reservation vide utilisé pour faire des trous dans l'afficahge en HTML'''
    agenda = []
    for day in week:
        reservations = reservable.checkDate(day)
        dayAgenda = []
        for reservation in reservations:
            dayAgenda.append([100*((timeToMinutes(reservation.end)-timeToMinutes(reservation.start))/(24*60)),
                              reservation.name, reservation.start.time(), reservation.end.time(), reservation.user])
        current = 0
        schedule = []
        for reservation in dayAgenda:
            if (reservation[0] != current):
                schedule.append(
                    [100*(timeToMinutes(reservation[2]) - current)/(24*60), None, None, None, None])
            schedule.append(reservation)
            current = timeToMinutes(reservation[3])
        agenda.append(schedule)
    print(agenda)
    return agenda


def timeToMinutes(time):
    return time.hour*60+time.minute


@app.route('/reset', methods=["GET", "POST"])
def reset():
    ''' Sur ce endpoint, on reset la base de données'''
    if session.get('logged_in') :
        clear_database()
        session.clear()
        initApp()
        redirect(url_for('home'))
    return flask.render_template("login.html.jinja2")

@app.route('/contact', methods=["GET"])
def contact():
    if session.get('logged_in') :
        return flask.render_template("contact.html.jinja2")
    return flask.render_template("login.html.jinja2")

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
