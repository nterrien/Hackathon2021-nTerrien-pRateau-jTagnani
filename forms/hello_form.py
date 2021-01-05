# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# Creation d'une classe heritant de 'flask_wtf.Form'
class HelloForm(FlaskForm):
    name = StringField("Nom : ", validators=[DataRequired()])
