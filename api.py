import sqlite3
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime

# Connect to database
def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

# Create tables
def create_tables():
    err = ""
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS meters''')
        cur.execute('''DROP TABLE IF EXISTS meter_data''')
        cur.execute('''CREATE TABLE meters (id INTEGER PRIMARY KEY NOT NULL, label TEXT NOT NULL)''')
        cur.execute('''CREATE TABLE meter_data (id INTEGER PRIMARY KEY NOT NULL, meter_id INTEGER NOT NULL, timestamp TIMESTAMP NOT NULL, value INTEGER NOT NULL, FOREIGN KEY (meter_id) REFERENCES meters (id))''')
        conn.commit()
        cur.close()
    except: 
        err = "Error creating tables"
        conn.rollback()
    finally:
        conn.close()
        return err   

def insert_data():
    err = ""
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO meters VALUES (1, 'test')")
        cur.execute("INSERT INTO meters VALUES (2, 'test2')")
        cur.execute("INSERT INTO meters VALUES (3, 'test3')")
        cur.execute("INSERT INTO meters VALUES (4, 'test4')")
        cur.execute("INSERT INTO meters VALUES (5, 'test5')")
        cur.execute("INSERT INTO meter_data (id, meter_id, timestamp, value) VALUES (?, ?, ?, ?)", (100, 1, datetime.datetime.now(), 11))
        cur.execute("INSERT INTO meter_data (id, meter_id, timestamp, value) VALUES (?, ?, ?, ?)", (200, 2, datetime.datetime.now(), 22))
        cur.execute("INSERT INTO meter_data (id, meter_id, timestamp, value) VALUES (?, ?, ?, ?)", (300, 3, datetime.datetime.now(), 33))
        cur.execute("INSERT INTO meter_data (id, meter_id, timestamp, value) VALUES (?, ?, ?, ?)", (400, 4, datetime.datetime.now(), 44))
        cur.execute("INSERT INTO meter_data (id, meter_id, timestamp, value) VALUES (?, ?, ?, ?)", (500, 5, datetime.datetime.now(), 55))
        conn.commit()
        cur.close()
    except:
        err = "Error inserting data"
        conn().rollback()
    finally:
        conn.close()
        return err


def get_all_meters():
    meters = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM meters")
        meters = cur.fetchall()
        cur.close()
    except:
        meters = []
    return meters

def get_meters_by_id(id):
    data = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM meters WHERE id = ?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        # convert row object to dictionary
        data["id"] = row["id"]
        data["label"] = row["label"]
    except:
        data = {}
    return data

def get_meter_by_id(id):
    data = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM meter_data WHERE meter_id = ?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        # convert row object to dictionary
        data["id"] = row["id"]
        data["meter_id"] = row["meter_id"]
        data["timestamp"] = row["timestamp"]
        data["value"] = row["value"]
    except:
        data = {}
    return data

err = create_tables()
if err == "":
    print("Tables created")
else:
    print(err)
    SystemExit  
errr = insert_data()
if errr == "":
    print("Data inserted")
else:
    print(errr)
    SystemExit 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/meters', methods=['GET'])
def api_get_meters():
    return render_template('index.html', Result=get_all_meters())

@app.route('/api/meters/<id>', methods=['GET'])
def api_get_meter(id):
    return jsonify(get_meter_by_id(id))

@app.route('/api/meters/<id>/data', methods=['GET'])
def api_get_meterss(id):
    return get_meters_by_id(id)

if __name__ == "__main__":
    # app.debug = True
    # app.run(debug=True)
    app.run()