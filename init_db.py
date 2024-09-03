import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('school.db')

# Create a cursor object
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    parent_contact TEXT NOT NULL
)
''')

# Create marks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    mark INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id)
)
''')

# Insert sample data into students table
students_data = [
    (1, 'Ketan Joshi', '+919557871523'),
    (2, 'Helen Saint', '+142455225'),
    (3, 'Emily Davis', '+1234567892'),
    (4, 'Michael Brown', '+1234567893')
]

cursor.executemany('''
INSERT INTO students (student_id, name, parent_contact)
VALUES (?, ?, ?)
''', students_data)

# Insert sample data into marks table
marks_data = [
    (1, 'Math', 75),
    (1, 'English', 45),
    (2, 'Math', 85),
    (2, 'English', 55),
    (3, 'Math', 56),
    (3, 'English', 65),
    (4, 'Math', 90),
    (4, 'English', 70)
]

cursor.executemany('''
INSERT INTO marks (student_id, subject, mark)
VALUES (?, ?, ?)
''', marks_data)


# Commit and close the connection
conn.commit()
conn.close()

print("Database initialized and sample data inserted successfully.")
