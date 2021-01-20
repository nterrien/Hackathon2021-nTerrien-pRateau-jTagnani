from flask import Flask, flash, request, redirect, url_for, make_response, session, abort
import flask  # BSD License (BSD-3-Clause)
import os
from werkzeug.utils import secure_filename
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import WashingMachine
from bdd.dbMethods import addUser, findUser, updateUser
from datetime import datetime, date


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

''' Initialise la base de données et la liste des machines disponibles'''
def initApp ():
    init_database()
    global machineList
    machineList = []
    for id in range (4):
        machineList.append (WashingMachine (id))


with app.app_context():
    initApp ()


''' Trouve la machine correspondant à l'id et renvoie un 404 sinon'''
def findMachine (id):
    id = int (id)
    l = filter (lambda m : m.index == id, machineList)
    try :
        return next(l)
    except Exception as e:
        print(e)
        abort(404)

@app.route('/', methods=["GET", "POST"])
def home():
    return flask.render_template("home.html.jinja2")

''' Sur ce endpoint, on reset la base de données'''
@app.route('/reset', methods=["GET", "POST"])
def reset():
    clear_database()
    initApp ()
    return flask.render_template("home.html.jinja2")

## Pages pour montrer le fonctionnement de WashingMachine
''' Imprime la liste des machines à laver (ce sont des objet dons pas beaux...)
    Nicolas si besoin tu devrais pouvoir avoir leur nom avec machine.label et leur index avec machine.index'''
@app.route('/machine/findAll', methods=["GET", "POST"])
def findAllMachines():
    print (machineList)
    return flask.render_template("home.html.jinja2")

''' Accède à la machine id et regarde les réservations sur une journée à passer en paramètre (type date)'''
@app.route('/machine/<id>/check', methods=["GET", "POST"])
def check(id):
    machine = findMachine (id)
    print (machine.checkDate(date.today()))
    return flask.render_template("home.html.jinja2")

''' Accède à la machine id et regarde les réservations de tous les tempss '''
@app.route('/machine/<id>/findAll', methods=["GET", "POST"])
def findAllReservations(id):
    machine = findMachine (id)
    print (machine.findAll())
    return flask.render_template("home.html.jinja2")

''' réserve la machine pour un créneau d'une durée prédéfinie pour une horodate '''
@app.route('/machine/<id>/reserve', methods=["GET", "POST"])
def reserve(id):
    machine = findMachine (id)
    machine.reserve(datetime.today())
    return flask.render_template("home.html.jinja2")

## Pages pour montrer le fonctionnement de User
@app.route('/user/create', methods=["GET", "POST"])
def create():
    addUser ("admin", "password")
    return flask.render_template("home.html.jinja2")

@app.route('/user/find', methods=["GET", "POST"])
def find():
    print (findUser("admin"))
    return flask.render_template("home.html.jinja2")

@app.route('/user/update', methods=["GET", "POST"])
def update():
    user = findUser("admin")
    updateUser (user, "admin2", "new password")
    return flask.render_template("home.html.jinja2")



@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
