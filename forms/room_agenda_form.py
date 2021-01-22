# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.core import DateField, SelectField

class RoomAgendaForm(FlaskForm):
    reservable = SelectField("Salle", coerce=str)
    date = DateField("Jour", format="%d/%m/%Y")
