from flask import Flask, flash, request, redirect, url_for, make_response, session
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
import flask  # BSD License (BSD-3-Clause)
import os
import hashlib
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('config')



#db.init_app(app)

# with app.app_context():
#     init_database()

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
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
        else:
            flash('wrong password!')
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
    if request.method == 'POST':
        #Ajout des données dans la bdd
        session['logged_in'] = True
        return redirect(url_for('home'))
    return flask.render_template("signin.html.jinja2")

@app.route("/isSigned",  methods=["POST"])
def isSigned():
    result = request.form
    u = result['username']
    p = result['password']
    b = p.encode('utf-8')
    salt = os.urandom(16)
    hash = hashlib.pbkdf2_hmac('sha256', b, salt, 100000)
    if False:
        session['logged_in']=True
    else :
        session['logged_in']=False
    return flask.url_for('home')


@app.route('/general', methods=["GET", "POST"])
def general():
    if not session.get('logged_in'):
        return flask.render_template('login.html.jinja2')
    else:
        return flask.render_template("general.html.jinja2")
    

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
