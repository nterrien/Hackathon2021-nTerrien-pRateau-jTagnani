from flask import Flask, flash, request, redirect, url_for, make_response, session
import flask  # BSD License (BSD-3-Clause)
import os
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from forms.washing_machine_form import WashingMachineForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import getMachineList, initWashingMachineList, findMachineWith404
from bdd.objects.room import roomList, initRoomList, findRoomWith404
from bdd.dbMethods import addUser, findUser, updateUser


app = Flask(__name__)
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


@app.route('/', methods=["GET", "POST"])
def home():
    return flask.render_template("home.html.jinja2")


@app.route('/washing', methods=["GET", "POST"])
def washing():
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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
