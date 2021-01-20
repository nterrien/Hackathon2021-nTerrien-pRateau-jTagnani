from flask import Flask, flash, request, redirect, url_for, make_response, session
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
from wtforms.validators import DataRequired, EqualTo
import flask  # BSD License (BSD-3-Clause)
import os
import hashlib
from werkzeug.utils import secure_filename
from bdd.database import db, init_database, populate_database, clear_database
from bdd.objects.washingMachine import WashingMachine
from bdd.dbMethods import addUser, findUser, updateUser
from datetime import datetime, date


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

with app.app_context():
    init_database()
    machine = WashingMachine ("1")

# Route de base qui conduit à Login si l'utilisateur n'est pas identifié et à home si il l'est
@app.route('/', methods=["GET", "POST"])
def home():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        return flask.render_template("home.html.jinja2")

# Page de login
@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Bon id/mdp ?
        result = request.form
        username = result['username']
        if findUser(username) == None :
            flash('wrong username')
            return flask.render_template("login.html.jinja2")
        user = findUser(username)
        password = user.password
        print (findUser(username).password)
        passw = result['password']
        byPassword = passw.encode('utf-8')
        salt = os.urandom(16)
        hashPassword = hashlib.pbkdf2_hmac('sha256', byPassword, salt, 100000)
        print(hashPassword)
        
        if passw == password :
            session['username'] = username
            session['logged_in'] = True
        else:
            flash('wrong password!')
        print(session.get('username'))    
        return redirect(url_for('home'))
    else :
        return flask.render_template("login.html.jinja2")    
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
        byPassword = password.encode('utf-8')
        salt = os.urandom(16)
        hashPassword = hashlib.pbkdf2_hmac('sha256', byPassword, salt, 100000)
        print(hashPassword)
        hashPasswor = hashlib.pbkdf2_hmac('sha256', byPassword, salt, 100000)
        print(hashPasswor)
        if findUser(username) == None :
            addUser(username, Password)
            session['logged_in'] = True
        else :
            flash('Oups ! Sign in failed, user already exists')
        return redirect(url_for('home'))
    else :
        flash('Username must have between 4 and 25 characters')
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

@app.route('/changePassword', methods=["GET", "POST"])
def change():
    form = ChangePassword(request.form)
    result=request.form
    if request.method == 'POST':
        print(result['password'])
        if form.validate() : 
            result=request.form
            
            username = session.get('username')
            print(session.get('username'))
            print(result['password'])
            user = findUser(username)
            updateUser (user, username, result['password'])
            return flask.render_template("home.html.jinja2")
        else :
            flash('Issue')    
    return flask.render_template('changePassword.html.jinja2')

@app.route('/profil', methods=["GET"])
def profil():
    return flask.render_template('profil.html.jinja2')    


@app.route('/general', methods=["GET", "POST"])
def general():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        return flask.render_template("general.html.jinja2")
    

## Pages pour montrer le fonctionnement de WashingMachine
@app.route('/machine/check', methods=["GET", "POST"])
def check():
    print (machine.checkDate(date.today()))
    return flask.render_template("home.html.jinja2")

@app.route('/machine/findAll', methods=["GET", "POST"])
def findAll():
    print (machine.findAll())
    return flask.render_template("home.html.jinja2")

@app.route('/machine/reserve', methods=["GET", "POST"])
def reserve():
    machine.reserve(datetime.today())
    return flask.render_template("home.html.jinja2")

## TODO: Pages pour montrer le fonctionnement de User
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
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
