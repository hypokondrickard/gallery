from os import listdir, makedirs, getcwd, walk
from os.path import isfile, join, exists, isdir
import os, fnmatch
import pyexiv2
import sys
import re
import math
import __future__
import sqlite3

conn = sqlite3.connect('/tmp/gallery.db')
c = conn.cursor()
c.execute('''CREATE TABLE bilder (primkey,filename,year,month,day,lon,lat,ctimestamp)''')

def gps2Num(coordParts):
    # will calculate the value of divison-split WGS84 coordinates
    #parts = str(coordParts).explode('/')

    parts = str(coordParts).split("/")

    if(len(parts) <= 0):
        return float(0)
    if(len(parts) == 1):
        return float(parts[0])

    return float(parts[0]) / float(parts[1])

def getGps(exifCoordinput):
    exifCoord = []
    exifCoord = exifCoordinput.split(" ")

    if len(exifCoord) == 3:
        degrees = gps2Num(exifCoord[0])
        minutes = gps2Num(exifCoord[1])
        seconds = gps2Num(exifCoord[2])
    elif len(exifCoord) == 2:
        degrees = gps2Num(exifCoord[0])
        minutes = gps2Num(exifCoord[1])
        seconds = 0
    elif len(exifCoord) == 1:
        degrees = gps2Num(exifCoord[0])
        minutes = 0
        seconds = 0
    else:
        degrees = 0
        minutes = 0
        seconds = 0

    #normalize
    minutes += 60 * (degrees - math.floor(degrees))
    degrees = math.floor(degrees)
    seconds += 60 * (minutes - math.floor(minutes))
    minutes = math.floor(minutes)

    #extra normalization, probably not necessary unless you get weird data
    if(seconds >= 60):
        minutes += math.floor(seconds/60.0)
        seconds -= 60*math.floor(seconds/60.0)

    if(minutes >= 60):
        degrees += math.floor(minutes/60.0)
        minutes -= 60*math.floor(minutes/60.0)

    return degrees+(((minutes * 60) + seconds + (seconds - math.floor(seconds))*60)/3600)


path_name = sys.argv[1]

files = []
for root, dirnames, filenames in os.walk(path_name):
  for filename in filenames:
    files.append(os.path.join(root, filename))
 

#database key, will be incremented after each insert 
primkey = 0

for image in files:
    if "JPG" not in image: continue

    year = month = day = longitude = latitude = 0
    try:
        metadata = pyexiv2.ImageMetadata(image)
        metadata.read()
    except KeyError:
        pass

    datestr = str(metadata['Exif.Photo.DateTimeOriginal'].raw_value)

    m = re.match("(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})", datestr)
    day = int(m.group(3))
    month = int(m.group(2))
    year = int(m.group(1))

    try:
        longitude =  getGps(metadata['Exif.GPSInfo.GPSLongitude'].raw_value)
        latitude = getGps(metadata['Exif.GPSInfo.GPSLatitude'].raw_value)
    except KeyError:
        pass

    filename = image
    #print year+month+day
    #print longitude
    #print latitude
    #print("ar: %d manad: %d dag: %d" % (year, month, day))
    sql = "insert into bilder (primkey, filename, year, month, day, lon, lat, ctimestamp) values ('%d', '%s', '%d', '%d', '%d','%f','%f','0');" % (primkey, filename , year, month, day, longitude, latitude)
    c.execute(sql)
    primkey = primkey+1


conn.commit()
conn.close()
