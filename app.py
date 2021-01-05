from flask import Flask
import flask  # BSD License (BSD-3-Clause)
from forms.hello_form import HelloForm

app = Flask(__name__)
app.config.from_object('config')

# db.init_app(app)

# with app.app_context():
#     init_database()


@app.route('/', methods=["GET", "POST"])
def home():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        return flask.redirect(flask.url_for('helloW', name = name))
    else:
        return flask.render_template("home.html.jinja2", form=form)

@app.route('/hello/<name>')
def helloW(name):
    return flask.render_template("hello.html.jinja2", name=name)

@app.route('/about')
def about():
    return flask.render_template("about.html.jinja2")


@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404

if __name__ == '__main__':
    app.run()
