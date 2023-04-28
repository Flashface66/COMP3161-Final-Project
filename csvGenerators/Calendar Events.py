import csv
import mysql.connector
import os
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)

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

allevents = os.path.join('./csvs', 'calendarevents.csv')
with open(allevents, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['assignment_id', 'course_id', 'event_name', 'date'])
    for event in calendar:
        writer.writerow(event)


# Commit the changes to the database
db.commit()

# Close the database connection
db.close()