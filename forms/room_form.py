# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.fields.core import FormField
from forms.room_agenda_form import RoomAgendaForm
from forms.room_reservation_form import RoomReservationForm


class RoomForm(FlaskForm):
    agenda = FormField(RoomAgendaForm)
    reservation = FormField(RoomReservationForm)
