# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.core import DateField, SelectField

# Creation d'une classe heritant de 'flask_wtf.Form'


class WashingMachineForm(FlaskForm):
    machine = SelectField("Machine : ", coerce=int)
    date = DateField("Jour", format="%d/%m/%Y")
