import sqlite3
import datetime

DB_FILE = "network.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # table for all devices
    c.execute('''CREATE TABLE IF NOT EXISTS devices
                 (ip TEXT PRIMARY KEY, mac TEXT, hostname TEXT, 
                  os_info TEXT, last_seen TIMESTAMP, type TEXT)''')
    conn.commit()
    conn.close()

def upsert_device(ip, mac, dev_type="Unknown"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.datetime.now()
    # check if device exists
    c.execute("SELECT * FROM devices WHERE ip=?", (ip,))
    data = c.fetchone()
    if data:
        c.execute("UPDATE devices SET last_seen=? WHERE ip=?", (now, ip))
    else:
        c.execute("INSERT INTO devices (ip, mac, hostname, os_info, last_seen, type) VALUES (?, ?, ?, ?, ?, ?)",
                  (ip, mac, "Scanning...", "Unknown", now, dev_type))
    conn.commit()
    conn.close()

def update_device_details(ip, hostname, os_info):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE devices SET hostname=?, os_info=? WHERE ip=?", (hostname, os_info, ip))
    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect(DB_FILE)
    # returns results als list from dictionaries
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]