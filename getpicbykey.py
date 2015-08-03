import sqlite3
import sys

def main(pickey):
    #print "%s %s %s " % (year, month, day)
    # do whatever and return 0 for success and an 
    # integer x, 1 <= x <= 256 for failure
    conn = sqlite3.connect("/tmp/gallery.db")
    c = conn.cursor()

    sql = "SELECT * FROM bilder WHERE primkey='%s'" % (pickey)
    
#    picdetails = []
#    for row in c.execute(sql):
#        picdetails.append(row)
    c.execute(sql)
    resultat = c.fetchone()
    conn.close()
    return resultat

if __name__=='__main__':
    sys.exit(main(sys.argv[1]))