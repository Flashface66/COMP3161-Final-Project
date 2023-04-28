import random
import os
import csv
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)


cursor = db.cursor()
cursor.execute("USE notquiteourvle")
cursor.execute("DROP TABLE IF EXISTS calendar_events")


cursor.execute("""CREATE TABLE calendar_events (
    event_id INT AUTO_INCREMENT NOT NULL,
    assignment_id INT NULL,
    course_id VARCHAR(50),
    event_name VARCHAR (500),
    due_date DATETIME,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    PRIMARY KEY (event_id)
)""")

cursor.execute("SET FOREIGN_KEY_CHECKS=0")
calevents = os.path.join('./csvs', 'calendarevents.csv')
with open(calevents, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query =  "INSERT INTO calendar_events (assignment_id, course_id, event_name, due_date) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3])
        cursor = db.cursor()
        cursor.execute(query, values)

cursor.execute("SET FOREIGN_KEY_CHECKS=1")

sql_query = """LOAD DATA LOCAL INFILE './calendarevents.csv'
               INTO TABLE calendar_events
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id, course_id, event_name, due_date);"""


calendar = os.path.join('./sqlFiles', 'load_calendar.sql')
with open(calendar, "w") as f:
    f.write(sql_query)


db.commit()
db.close()
