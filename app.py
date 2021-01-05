from flask import Flask
import flask  # BSD License (BSD-3-Clause)

app = Flask(__name__)
app.config.from_object('config')

# db.init_app(app)

# with app.app_context():
#     init_database()


@app.route('/', methods=["GET", "POST"])
def hellow():
    return flask.render_template("hello.html.jinja2")


if __name__ == '__main__':
    app.run()
