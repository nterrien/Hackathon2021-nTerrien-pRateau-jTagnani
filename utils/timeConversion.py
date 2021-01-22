from datetime import datetime


def datetimeToString (dt):
    return dt.strftime ('%Y-%m-%d %H:%M')

def datetimeFromString (text):
    return datetime.strptime (text, '%Y-%m-%d %H:%M')

def timeToMinutes(time):
    return time.hour*60+time.minute

def getDayWeek(day):
    weekday = day.isoweekday()
    start = day - timedelta(days=weekday-1)
    dates = [start + timedelta(days=d) for d in range(7)]
    return dates