import sqlite3

DATABASE = 'hospital.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  patient_id INTEGER,
                  doctor TEXT NOT NULL,
                  booth TEXT NOT NULL,
                  date TEXT NOT NULL,
                  time TEXT NOT NULL,
                  FOREIGN KEY (patient_id) REFERENCES patients (id))''')
    
    conn.commit()
    conn.close()

def add_patient(name, email, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, email, password) VALUES (?, ?, ?)",
              (name, email, password))
    conn.commit()
    conn.close()

def get_patient(identifier, password=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if password:
        c.execute("SELECT * FROM patients WHERE email = ? AND password = ?", (identifier, password))
    else:
        c.execute("SELECT * FROM patients WHERE id = ?", (identifier,))
    
    patient = c.fetchone()
    conn.close()
    return patient

def add_appointment(patient_id, doctor, booth, date, time):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO appointments (patient_id, doctor, booth, date, time) VALUES (?, ?, ?, ?, ?)",
              (patient_id, doctor, booth, date, time))
    conn.commit()
    conn.close()

def get_appointments(patient_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    appointments = c.fetchall()
    conn.close()
    return appointments