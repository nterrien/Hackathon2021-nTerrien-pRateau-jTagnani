# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.core import DateField, StringField, TimeField
from wtforms import validators

# Creation d'une classe heritant de 'flask_wtf.Form'


class WashingMachineReservationForm(FlaskForm):
    startDate = DateField("Jour : ", [
        validators.DataRequired()], format="%d/%m/%Y")
    startHour = TimeField("Heure de début")