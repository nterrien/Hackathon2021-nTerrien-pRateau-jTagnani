from flask import Flask, flash, request, redirect, url_for, make_response, session
import flask  # BSD License (BSD-3-Clause)
import os
from werkzeug.utils import secure_filename
from datetime import datetime, date
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from forms.washing_machine_form import WashingMachineForm
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import WashingMachine

washingmachineWithoutDB = [{'name': "1"}, {
    'name': "2"}, {'name': "3"}, {'name': "4"}]

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
    fausseresultatDB = [{'id': 1}, {'id': 2}]
    form = WashingMachineForm(obj=fausseresultatDB)
    form.machine.choices = [(g['id']) for g in fausseresultatDB]
    if form.validate_on_submit():
        return flask.render_template("washing.html.jinja2", form=form)
    else:
        form.date.data = date.today()
        return flask.render_template("washing.html.jinja2", form=form)


@app.route('/check', methods=["GET", "POST"])
def check():
    print(machine.checkDate(date.today()))
    return flask.render_template("home.html.jinja2")


@app.route('/findAll', methods=["GET", "POST"])
def find():
    print(machine.findAll())
    return flask.render_template("home.html.jinja2")


@app.route('/reserve', methods=["GET", "POST"])
def reserve():
    machine.reserve(datetime.today())
    return flask.render_template("home.html.jinja2")


@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
