import urllib2
import sqlite3
import json
import time

URL = 'http://192.168.137.1:9000/update'
LINE = 'TEST'


def query_db(id):
    conn = sqlite3.connect('/tmp/factory.db')
    c = conn.cursor()
    record = {'line':LINE, 'station':id, 'timestamp':[]}
    c.execute('SELECT timestamp FROM prodline WHERE (station = %d AND sync = 0)'%id)
    try:
        while True:
            ttuple = time.strptime(c.next()[0], '%Y-%m-%d %H:%M:%S')
            t = int(time.mktime(ttuple))
            record['timestamp'].append(t)
    except:
        pass
    conn.close()
    return record        

    
def update_db(id):
    conn = sqlite3.connect('/tmp/factory.db')
    c = conn.cursor()
    c.execute('UPDATE prodline SET sync = 1 WHERE (station = %d AND sync = 0)'%id)
    conn.commit()
    conn.close()
    
    
if __name__ == '__main__':
    while True:
        for id in [1,2,3,4]:
            record = query_db(id)
            if len(record['timestamp']) > 0:
                data = json.dumps(record)
                req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})
                f = urllib2.urlopen(req)
                resp = f.read()
                f.close()
                print resp
                update_db(id)
        time.sleep(60)

