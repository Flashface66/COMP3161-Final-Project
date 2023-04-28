import csv
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root", password="Passwordnt")

cursor = db.cursor()

cursor.execute("USE notquiteourvle")


cursor.execute("""CREATE INDEX idx_assignment_id ON assignments (assignment_id)""")

cursor.execute("""CREATE TABLE calendar_events (
    event_id INT AUTO_INCREMENT,
    assignment_id INT NULL,
    course_id VARCHAR(50),
    event_name VARCHAR (500),
    due_date DATETIME,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    PRIMARY KEY (event_id)
)""")