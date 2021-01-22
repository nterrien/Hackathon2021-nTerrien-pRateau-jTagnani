from flask import request, render_template

from utils.timeConversion import timeToMinutes, getDayWeek
from forms.room_form import RoomForm
from datetime import date


def reservation_general(reservableListMethods, findReservablewith404, reservationMethod, reservable_type, template_name, username):
    form = RoomForm(obj=reservableListMethods())
    form.agenda.reservable.choices = [
        g.index for g in reservableListMethods()]
    if "reservation" in request.form and form.reservation.validate(form):
        success = reservationMethod(form)
        form.agenda.date.data = form.reservation.startDate.data
        return render_template(template_name, form=form, week=getDayWeek(form.reservation.startDate.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=username, reservable_type=reservable_type)
    elif "agenda" in request.form and form.agenda.validate(form):
        form.reservation.startDate.data = form.agenda.date.data
        return render_template(template_name, form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=username, reservable_type=reservable_type)
    else:
        form.agenda.reservable.data = reservableListMethods()[0].index
        form.agenda.date.data = date.today()
        form.reservation.startDate.data = form.agenda.date.data
        return render_template(template_name, form=form, week=getDayWeek(form.agenda.date.data), agenda=getReservationWeek(getDayWeek(form.agenda.date.data), findReservablewith404(form.agenda.reservable.data)), username=username, reservable_type=reservable_type)


def getReservationWeek(week, reservable):
    '''Les données retournées sont une liste avec chaque element qui correspond à un jour de la semaine
    Chaque jour est une liste de reservations composé de le % de la journée que represente cette reservation, le nom du reservant, l'heure de debut, l'heure de fin.
    Si None est le nom du reservant cela signifie que c'est une reservation vide utilisé pour faire des trous dans l'afficahge en HTML'''
    agenda = []
    for day in week:
        reservations = reservable.checkDate(day)
        dayAgenda = []
        for reservation in reservations:
            dayAgenda.append([100*((timeToMinutes(reservation.end)-timeToMinutes(reservation.start))/(24*60)),
                              reservation.name, reservation.start.time(), reservation.end.time(), reservation.user])
        current = 0
        schedule = []
        for reservation in dayAgenda:
            if (reservation[0] != current):
                schedule.append(
                    [100*(timeToMinutes(reservation[2]) - current)/(24*60), None, None, None, None])
            schedule.append(reservation)
            current = timeToMinutes(reservation[3])
        agenda.append(schedule)
    print(agenda)
    return agenda
