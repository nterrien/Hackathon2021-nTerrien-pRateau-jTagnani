from flask import Flask, flash, request, redirect, url_for, make_response, session
import flask  # BSD License (BSD-3-Clause)
import os
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from forms.washing_machine_form import WashingMachineForm
from forms.washing_machine_reservation_form import WashingMachineReservationForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import WashingMachine

app = Flask(__name__)
Bootstrap(app)
datepicker(app)
app.config.from_object('config')

db.init_app(app)

with app.app_context():
    init_database()
    machine = WashingMachine("1")


@app.route('/', methods=["GET", "POST"])
def home():
    return flask.render_template("home.html.jinja2")


@app.route('/washing', methods=["GET", "POST"])
def washing():
    # Appel à la database TODO
    fausseresultatDB = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]
    form = WashingMachineForm(obj=fausseresultatDB)
    form.machine.choices = [(g['id']) for g in fausseresultatDB]
    reservationForm = WashingMachineReservationForm()
    if reservationForm.validate_on_submit():
        # TODO choix e la machine avec form.machine.data
        machine.reserve(datetime.combine(
            reservationForm.startDate.data, reservationForm.startHour.data))
        form.date.data = reservationForm.startDate.data
        return flask.render_template("washing.html.jinja2", form=form, reservationForm=reservationForm, week=getDayWeek(reservationForm.startDate.data), agenda=getReservationWeek(getDayWeek(form.date.data), machine))
    elif form.validate_on_submit():
        reservationForm.startDate.data = form.date.data
        reservationForm.endDate.data = form.date.data
        return flask.render_template("washing.html.jinja2", form=form, reservationForm=reservationForm, week=getDayWeek(form.date.data), agenda=getReservationWeek(getDayWeek(form.date.data), machine))
    else:
        form.machine.data = fausseresultatDB[0]['id']
        form.date.data = date.today()
        reservationForm.startDate.data = form.date.data
        reservationForm.endDate.data = form.date.data
        return flask.render_template("washing.html.jinja2", form=form, reservationForm=reservationForm, week=getDayWeek(form.date.data), agenda=getReservationWeek(getDayWeek(form.date.data), machine))


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


@ app.route('/check', methods=["GET", "POST"])
def check():
    print(machine.checkDate(date.today()))
    return flask.render_template("home.html.jinja2")


@ app.route('/findAll', methods=["GET", "POST"])
def find():
    print(machine.findAll())
    return flask.render_template("home.html.jinja2")


@ app.route('/reserve', methods=["GET", "POST"])
def reserve():
    machine.reserve(datetime.today())
    return flask.render_template("home.html.jinja2")


@ app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
