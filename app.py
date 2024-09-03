from flask import Flask, request, render_template, redirect, url_for, flash
from twilio.rest import Client
import sqlite3

app = Flask(__name__)
app.secret_key = '3EIOW8'

# Configure Twilio
account_sid = 'ACa182f33abfbd87e9348da2177cbf229e'
auth_token = 'ebb4b937882dccbcdcb1c48d32dbcfd3'
twilio_number = '+13345648896'
client = Client(account_sid, auth_token)

# Function to send SMS using Twilio
def send_sms(to, message):
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to
        )
        print(f"Message sent with SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False

# Function to fetch student information from SQLite database
def get_student_info(student_id):
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, parent_contact FROM students WHERE student_id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        if student:
            return {"name": student[0], "parent_contact": student[1]}
        else:
            return None
    except Exception as e:
        print(f"Failed to fetch student info: {e}")
        return None

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling marks submission
@app.route('/marks', methods=['GET', 'POST'])
def marks():
    if request.method == 'POST':
        try:
            student_id = request.form['student_id']
            subject = request.form['subject']
            mark = int(request.form['mark'])
            
            # Fetch student information from database
            student = get_student_info(student_id)
            if not student:
                flash('Student not found. Please check the student ID.', 'danger')
                return redirect(url_for('marks'))
            
            # Process marks and send alert if mark is below threshold
            if mark < 33:
                message = f"Your ward {student['name']} scored {mark} in {subject}."
                if send_sms(student['parent_contact'], message):
                    flash('Alert SMS sent successfully!', 'success')
                else:
                    flash('Failed to send alert SMS. Please try again later.', 'danger')
            
            # Save marks to database
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO marks (student_id, subject, mark) VALUES (?, ?, ?)",
                           (student_id, subject, mark))
            conn.commit()
            conn.close()
            
            flash('Marks submitted successfully!', 'success')
            return redirect(url_for('marks'))
        except Exception as e:
            print(f"Error processing form: {e}")
            flash('An error occurred while submitting the form. Please try again.', 'danger')
            return redirect(url_for('marks'))
    
    return render_template('marks.html')

# Route for viewing marks
@app.route('/view-data')
def view_data():
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT students.student_id, students.name, students.parent_contact, marks.subject, marks.mark FROM students JOIN marks ON students.student_id = marks.student_id")
        data = cursor.fetchall()
        conn.close()
        return render_template('view_data.html', data=data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        flash('An error occurred while fetching data. Please try again.', 'danger')
        return redirect(url_for('index'))

# Optionally, handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
