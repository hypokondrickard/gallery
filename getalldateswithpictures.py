import sqlite3
import sys
import datetime
import calendar

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
    print "uppdaterar datum"
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

def main(requestedyear):
    conn = sqlite3.connect("/tmp/gallery.db")
    c = conn.cursor()
    sql = "SELECT year,month,day FROM bilder WHERE year='%s' ORDER BY ctimestamp ASC" % (requestedyear)

    resultat = dict()

    for row in c.execute(sql):
        resultat = update_calendar(int(row[0]),int(row[1]),int(row[2]), resultat)

    conn.close()
    return resultat

if __name__=='__main__':
    sys.exit(main(sys.argv[1]))