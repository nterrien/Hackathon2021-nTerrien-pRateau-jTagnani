# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.core import DateField, SelectField, TimeField
from wtforms import validators

# Creation d'une classe heritant de 'flask_wtf.Form'


class WashingMachineReservationForm(FlaskForm):
    startDate = DateField("Jour du début", [
        validators.DataRequired()], format="%d/%m/%Y")
    startHour = TimeField("Heure de début", [
        validators.DataRequired()])
    endDate = DateField("Jour de fin", [
        validators.DataRequired()], format="%d/%m/%Y")
    endHour = TimeField("Heure de fin", [
        validators.DataRequired()])
