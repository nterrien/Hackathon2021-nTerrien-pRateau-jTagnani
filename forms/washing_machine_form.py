# Import des bibliotheque permettant de manipuler des formulaires HTML en Python
from flask_wtf import FlaskForm
from wtforms.fields.core import FormField
from forms.washing_machine_agenda_form import WashingMachineAgendaForm
from forms.washing_machine_reservation_form import WashingMachineReservationForm

class WashingMachineForm(FlaskForm):
    agenda = FormField(WashingMachineAgendaForm)
    reservation = FormField(WashingMachineReservationForm)
