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
cursor.execute("DROP TABLE IF EXISTS grades")
cursor.execute("DROP TABLE IF EXISTS submissions")

cursor.execute("DROP TABLE IF EXISTS assignments")


cursor.execute("""CREATE TABLE submissions (
    student_id INT,
    assignment_id INT,
    course_id VARCHAR(50),
    file VARCHAR(255),
    due_date DateTime,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    PRIMARY KEY (student_id, assignment_id, course_id),
    INDEX (assignment_id)
)""")

cursor.execute("""CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT,
    course_id VARCHAR(50),
    assignment_name VARCHAR(50),
    due_date DATETIME,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (assignment_id, course_id)
    
)""")

cursor.execute("""CREATE TABLE grades (
    student_id INT,
    course_id VARCHAR(50),
    grade DECIMAL(5,2) NOT NULL CHECK (grade >= 0 AND grade <= 100),
    assignment_id INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (assignment_id) REFERENCES submissions(assignment_id),
    PRIMARY KEY(student_id, assignment_id, course_id)
)""")

cursor.execute("""CREATE INDEX idx_assignment_id ON assignments (assignment_id)""")



cursor.execute("SET FOREIGN_KEY_CHECKS=0")
submissions = os.path.join('./csvs', 'submissions.csv')
with open(submissions, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query =  "INSERT INTO submissions (assignment_id, student_id, course_id, file, due_date) VALUES (%s, %s, %s, %s, %s)"
        values = (int(row[0]), int(row[1]), row[2], row[3], row[4])
        cursor = db.cursor()
        cursor.execute(query, values)

sql_query = """LOAD DATA LOCAL INFILE './submissions.csv'
               INTO TABLE submissions
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id, student_id, course_id, file, due_date);"""


studassignments = os.path.join('./sqlFiles', 'load_some_assignments.sql')
with open(studassignments, "w") as f:
    f.write(sql_query)


studgrades = os.path.join('./csvs', 'grades.csv')
with open(studgrades, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO grades (student_id, course_id, grade, assignment_id) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], int(row[3]))
        cursor = db.cursor()
        cursor.execute(query, values)


sql_query = """LOAD DATA LOCAL INFILE './grades.csv'
               INTO TABLE grades
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (student_id, course_id, grade, assignment_id);"""


somegrades = os.path.join('./sqlFiles', 'load_some_grades.sql')
with open(somegrades, "w") as f:
    f.write(sql_query)


allassignments = os.path.join('./csvs', 'assignments.csv')
with open(allassignments, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO assignments (assignment_id,course_id,assignment_name,due_date) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3])
        cursor = db.cursor()
        cursor.execute(query, values)
cursor.execute("SET FOREIGN_KEY_CHECKS=1")


sql_query = """LOAD DATA LOCAL INFILE './assignments.csv'
               INTO TABLE assignments
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id,course_id,assignment_name,due_date);"""


somegrades = os.path.join('./sqlFiles', 'load_hw.sql')
with open(somegrades, "w") as f:
    f.write(sql_query)

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()
