from datetime import datetime


def datetimeToString (dt):
    return dt.strftime ('%Y-%m-%d %H:%M')

def datetimeFromString (text):
    return datetime.strptime (text, '%Y-%m-%d %H:%M')
