import sqlite3
import sys
import datetime
import time
import calendar
from flask import g

def get_pics_by_date(year,month,day):

    datestr = "%s:%s:%s 00:00:00" % (year,month,day)
    date_obj_string = datetime.datetime.strptime(datestr, '%Y:%m:%d %H:%M:%S')
    tstamp_start = int(time.mktime(date_obj_string.timetuple()))
    tstamp_end = tstamp_start + 86400

    c = g.db.cursor()

    sql = "SELECT primkey FROM bilder WHERE ctimestamp BETWEEN %s and %s ORDER BY ctimestamp ASC" % (tstamp_start, tstamp_end)

    pickeys = []
    
    for row in c.execute(sql):
        pickeys.append(row)

    return pickeys

def get_pic_by_key(pickey):
    c = g.db.cursor()

    sql = "SELECT * FROM bilder WHERE primkey='%s'" % (pickey)
    c.execute(sql)
    resultat = c.fetchone()
    return resultat

def get_random():
    c = g.db.cursor()

    sql = "SELECT * FROM bilder ORDER BY RANDOM() LIMIT 1;"
    
    c.execute(sql)
    resultat = c.fetchone()
    return resultat


def get_calendar(year):

    def get_name_of_month(monthnumber):
        return monthnumber
        #return str(monthnumber)+" "+datetime.date(2015, int(monthnumber), 10).strftime('%B')
        if monthnumber is 1:
            return "Jan"
        elif monthnumber is 2:
            return "Feb"
        elif monthnumber is 3:
            return "Mar"
        elif monthnumber is 4:
            return "Apr"
        elif monthnumber is 5:
            return "Maj"
        elif monthnumber is 6:
            return "Jun"
        elif monthnumber is 7:
            return "Jul"
        elif monthnumber is 8:
            return "Aug"
        elif monthnumber is 9:
            return "Sep"
        elif monthnumber is 10:
            return "Oct"
        elif monthnumber is 11:
            return "Nov"
        else:
            return "Dec"
        
    def create_year():
        year = dict()
        for month in range(1,13):
            thismonth = dict()
            for dayslot in range(1,43):
                thismonth.update({dayslot:''})
            year.update({get_name_of_month(month): thismonth})
        return year

    def basefill_year(year,calendarDict):
        for month in range(1,13):

            for day in range(1, calendar.monthrange(year,month)[1]+1):
                datum = (day,0)
                calendarDict = update_date(year, month, day, datum, calendarDict)

        return calendarDict

    def update_date(picyear,picmonth,picday, value, calendarDict):
        weekdayoffset = datetime.date(picyear, picmonth, 1).weekday()
        calendarDict[picyear][get_name_of_month(picmonth)][picday+weekdayoffset] = value
        return calendarDict

    def update_calendar(picyear,picmonth,picday,calendarDict):
        if picyear not in calendarDict:
            calendarDict.update({picyear:create_year()})
            calendarDict = basefill_year(picyear, calendarDict)

        datum = (picday,1)

        calendarDict = update_date(picyear, get_name_of_month(picmonth),picday,datum,calendarDict)

        return calendarDict

    c = g.db.cursor()

    sql = "SELECT year,month,day FROM bilder WHERE year='%s' ORDER BY ctimestamp ASC" % (year)

    resultat = dict()

    for row in c.execute(sql):
        resultat = update_calendar(int(row[0]),int(row[1]),int(row[2]), resultat)

    return resultat