from flask import Flask, flash, request, redirect, url_for, make_response, session, render_template
from flask_hashing import Hashing
from os import urandom, environ
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from datetime import datetime, timedelta

from forms.login_forms import RegistrationForm, ChangePassword, UsernameForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.dbMethods import addUser, findUser, updateUser, updateUsername
from reservation.reservation import reservation_general, getReservationWeek
from reservation.objects.washingMachine import getMachineList, initWashingMachineList, findMachineWith404
from reservation.objects.room import getRoomList, initRoomList, findRoomWith404
from utils.timeConversion import timeToMinutes, getDayWeek
from forms.room_form import RoomForm
from forms.washing_machine_form import WashingMachineForm

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
    if not session.get('logged_in'):
        return render_template('login.html.jinja2')
    else:
        username = None
        if session.get('username') != None:
            username = session.get('username')
        return render_template("home.html.jinja2", username=username)

# Page de login
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login(): 
    if request.method == 'GET':
        return render_template("login.html.jinja2")
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Bon id/mdp ?
        result = request.form
        username = result['username']
        # On regarde si l'utilisateur correspondant au nom d'utilisateur existe
        if findUser(username) == None:
            flash('wrong username')
            return render_template("login.html.jinja2")
            # On trouce l'user correspondant
        user = findUser(username)
        hashPassword = user.password
        passw = result['password']
        # On compare avec la bdd
        if hashing.check_value(hashPassword, passw, salt='abcd'):
            session['username'] = username
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return redirect(url_for('home'))
    return render_template("login.html.jinja2")

# logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    # return home()
    return redirect(url_for('home'))

# Page pour s'inscrire sur le site
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        result = request.form
        username = result['username']
        password = result['password']
        # On hash le password avec un système qui donne tjs le même hash pour simplifier
        hashPassword = hashing.hash_value(password, salt='abcd')
        # On regarde si l'utilisateur existe déjà
        if findUser(username) == None:
            # Ajout des données dans la bdd
            addUser(username, hashPassword)
            print(hashPassword)
        else:
            flash('Oups ! Sign in failed, user already exists')
        session['username'] = username
        return redirect(url_for('do_admin_login'))
    return render_template("signin.html.jinja2")

# Page qui permet de modifier son mot de passe
@app.route('/changePassword', methods=["GET", "POST"])
def change():
    if not session.get('logged_in'):
        return render_template('login.html.jinja2')
    form = ChangePassword(request.form)
    result = request.form
    if request.method == 'POST':
        if form.validate():
            result = request.form
            # On récupère le nom de l'utilisateur
            username = session.get('username')
            user = findUser(username)
            # On compare le mdp de l'user avec celui qu'il rentre pour changer de mdp
            if hashing.check_value(user.password, result['oldPassword'], salt='abcd'):
                password = result['password']
                hashPassword = hashing.hash_value(password, salt='abcd')
                updateUser(user, username, hashPassword)
                return render_template("home.html.jinja2")
        else:
            flash('Issue')
    return render_template('changePassword.html.jinja2')

# Page qui permet de modifier son nom d'utilisateur et son mot de passe
@app.route('/profil', methods=["GET", "POST"])
def profil():
    if not session.get('logged_in'):
        return render_template('login.html.jinja2')
    form = UsernameForm(request.form)
    if request.method == 'POST' and form.validate():
        result = request.form
        username = session.get('username')
        # Utilisation des méthodes de la bdd pour trouver l'utilisateur et changer son mdp
        user = findUser(username)
        updateUsername(user, result['username'])
        user = result['username']
        session['username'] = user
        return redirect(url_for('profil'))
    if 'username' in session:
        username = None
        username = session.get('username')
        return render_template('profil.html.jinja2', username=username)


# Page de reservation des machines à laver
@app.route('/washing', methods=["GET", "POST"])
def washing():
    if not session.get('logged_in'):
        return render_template('login.html.jinja2')
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

    return reservation_general(WashingMachineForm, getMachineList, findMachineWith404, reserve_washingmachine,
                               "machine", "washing.html.jinja2", session['username'])

# Page de reservation des salles
@app.route('/room', methods=["GET", "POST"])
def room():
    if not session.get('logged_in'):
        return render_template('login.html.jinja2')
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

    return reservation_general(RoomForm, getRoomList, findRoomWith404, reserve_room,
                               "salle", "room.html.jinja2", session['username'])


@app.route('/reset', methods=["GET", "POST"])
def reset():
    ''' Sur ce endpoint, on reset la base de données'''
    if session.get('logged_in') :
        clear_database()
        session.clear()
        initApp()
        redirect(url_for('home'))
    return render_template("login.html.jinja2")

@app.route('/contact', methods=["GET"])
def contact():
    if session.get('logged_in') :
        return render_template("contact.html.jinja2")
    return render_template("login.html.jinja2")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.secret_key = urandom(16)
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
