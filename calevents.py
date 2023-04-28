import csv
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root", password="Passwordnt")

cursor = db.cursor()

cursor.execute("USE notquiteourvle")


cursor.execute("SELECT * FROM assignments")
currentevents = cursor.fetchall()

calendar = []
for event in currentevents:
    assignment_id = event[0]
    course_id = event[1]
    event_name = event[2]
    date = event[3]
    calendar.append([assignment_id,course_id,event_name,date])

for i in calendar:
    query = "INSERT INTO calendar_events (assignment_id, course_id,event_name,due_date) VALUES (%s, %s, %s, %s)"
    values = (int(i[0]), i[1], i[2], i[3])
    cursor = db.cursor()
    cursor.execute(query, values)


# Commit the changes to the database
db.commit()

# Close the database connection
db.close()