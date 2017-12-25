import sqlite3
import serial
import time


def init_db():
    ''' Initialize database '''
    conn = sqlite3.connect('/tmp/factory.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS prodline(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        station INTEGER, 
        timestamp REAL DEFAULT (datetime('now', 'localtime')),
        sync INTEGER DEFAULT 0
        )''')
    conn.commit()
    conn.close()

def record_db(station):
    ''' Record database '''
    conn = sqlite3.connect('/tmp/factory.db')
    c = conn.cursor()
    c.execute('INSERT INTO prodline(station) VALUES(%d)'%station)
    conn.commit()
    conn.close()

def init_mbed():
    ''' Open serial port '''
    ser = serial.Serial('/dev/ttyACM0')
    return ser

if __name__ == '__main__':
    init_db()
    mbed = init_mbed()
    while True:
        try:
            txt = mbed.readline()
            station = int(txt.strip().split('ID: ')[1])
            print('Got %d'%station)
            record_db(station)
        except:
            pass 
        time.sleep(1)

