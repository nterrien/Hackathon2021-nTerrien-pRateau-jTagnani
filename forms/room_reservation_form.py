# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.core import DateField, IntegerField, TimeField
from wtforms import validators

class RoomReservationForm(FlaskForm):
    startDate = DateField("Jour de reservation (veuillez choisir le jour)", [
        validators.DataRequired()], format="%d/%m/%Y")
    startHour = TimeField("Heure de début (format HH:MM)")
    duration = IntegerField("Durée de la reservation en minutes")
