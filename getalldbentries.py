import sqlite3
import sys

def main():
    #print "%s %s %s " % (year, month, day)
    # do whatever and return 0 for success and an 
    # integer x, 1 <= x <= 256 for failure
    conn = sqlite3.connect("/tmp/example.db")
    c = conn.cursor()

    sql = "SELECT * FROM bilder ORDER BY ctimestamp ASC"
    
    for row in c.execute(sql):
        print row

    conn.close()
if __name__=='__main__':
    sys.exit(main())