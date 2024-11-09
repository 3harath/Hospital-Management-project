from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, add_patient, get_patient, add_appointment, get_appointments
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            add_patient(name, email, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    patient = get_patient(email, password)
    if patient:
        session['patient_id'] = patient[0]
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('patient_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'patient_id' not in session:
        return redirect(url_for('index'))
    
    patient = get_patient(session['patient_id'])
    appointments = get_appointments(session['patient_id'])
    return render_template('dashboard.html', patient=patient, appointments=appointments)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'patient_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        doctor = request.form['doctor']
        booth = request.form['booth']
        date = request.form['date']
        time = request.form['time']
        
        add_appointment(session['patient_id'], doctor, booth, date, time)
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('book_appointment.html')

if __name__ == '__main__':
    app.run(debug=True)