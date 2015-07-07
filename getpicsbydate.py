import sqlite3
import sys

def main(year, month, day):
    #print "%s %s %s " % (year, month, day)
    # do whatever and return 0 for success and an 
    # integer x, 1 <= x <= 256 for failure
    conn = sqlite3.connect("/tmp/example.db")
    c = conn.cursor()

    sql = "SELECT primkey FROM bilder WHERE year='%s' AND month='%s' AND day='%s' ORDER BY ctimestamp ASC" % (year, month, day)
    
    pickeys = []
    for row in c.execute(sql):
        pickeys.append(row)

    conn.close()
    return pickeys

if __name__=='__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))