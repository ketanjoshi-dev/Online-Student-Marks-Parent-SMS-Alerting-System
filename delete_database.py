import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('school.db')

# Create a cursor object
cursor = conn.cursor()

# Create students table
cursor.execute('''
DROP TABLE students
''')

cursor.execute('''
DROP TABLE marks
''')

conn.commit()
conn.close()