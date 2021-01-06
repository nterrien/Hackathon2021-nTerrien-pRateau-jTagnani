from flask import Flask, request
import flask  # BSD License (BSD-3-Clause)
from bdd.database import db, init_database, populate_database, clear_database
from bdd.dbMethods import findAllVisitor, findNameUsage
from api.nameAPI import saveNameInfo
from forms.hello_form import HelloForm
from forms.randomWord_form import NumberWordForm
from src.calcul import randomWords


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

with app.app_context():
    init_database()


@app.route('/', methods=["GET", "POST"])
def home():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data.lower()
        saveNameInfo(name)
        return flask.redirect(flask.url_for('helloW', name=name))
    else:
        return flask.render_template("home.html.jinja2", form=form)


@app.route('/hello/<name>')
def helloW(name):
    usages = findNameUsage (name)
    return flask.render_template("hello.html.jinja2", name=name, usages=usages)


@app.route('/about')
def about():
    return flask.render_template("about.html.jinja2")


@app.route('/word', methods=["GET", "POST"])
def word():
    form = NumberWordForm()
    if form.validate_on_submit():
        words = randomWords(form.number.data)
        return flask.render_template("word.html.jinja2", form=form, words=words)
    return flask.render_template("word.html.jinja2", form=form)


@app.route('/visitors')
def visitors_list():
    return flask.render_template("visitors_list.html.jinja2", visitors=findAllVisitor())

@app.route('/reset')
def reset():
    clear_database()
    init_database()
    return flask.redirect(flask.url_for('home'))

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.run()
