# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


# Creation d'une classe heritant de 'flask_wtf.Form'
class NumberWordForm(FlaskForm):
    number = IntegerField("Nom : ", validators=[DataRequired()])
