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
cursor.execute("DROP TABLE IF EXISTS student_course")
cursor.execute("DROP TABLE IF EXISTS lect_course")


cursor.execute("""CREATE TABLE student_course (
  student_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students (student_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
)""")


cursor.execute("""CREATE TABLE lect_course (
  lect_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (lect_id, course_id),
  FOREIGN KEY (lect_id) REFERENCES lecturers (lect_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
)""")


studcourses = os.path.join('./csvs', 'student_course.csv')

with open(studcourses, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)


sql_query = """LOAD DATA LOCAL INFILE './student_courses.csv'
               INTO TABLE student_course
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (student_id, course_id);"""


studsubject = os.path.join('./sqlFiles', 'load_student_courses.sql')
with open(studsubject, "w") as f:
    f.write(sql_query)

lectcourses = os.path.join('./csvs', 'lecturer_course.csv')

with open(lectcourses, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO lect_course (lect_id, course_id) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)

sql_query = """LOAD DATA LOCAL INFILE './lecturer_course.csv'
               INTO TABLE lect_course
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (lect_id, course_id);"""


lecttaught = os.path.join('./sqlFiles', 'load_lect_courses.sql')
with open(lecttaught, "w") as f:
    f.write(sql_query)

db.commit()
db.close()