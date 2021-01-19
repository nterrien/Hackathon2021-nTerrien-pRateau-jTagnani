from flask import Flask, flash, request, redirect, url_for, make_response, session
import flask  # BSD License (BSD-3-Clause)
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('config')

#db.init_app(app)

# with app.app_context():
#     init_database()


@app.route('/', methods=["GET", "POST"])
def home():
    return flask.render_template("home.html.jinja2")

@app.errorhandler(404)
def not_found(e):
    return flask.render_template("404.html.jinja2"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
