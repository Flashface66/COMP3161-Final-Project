import csv
import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="root", password="Normal78")

cursor = mydb.cursor()
cursor.execute("DROP DATABASE IF EXISTS notquiteourvle")
cursor.execute("CREATE DATABASE notquiteourvle")
cursor.execute("USE notquiteourvle")

cursor.execute("""CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
)""")

cursor.execute("""CREATE TABLE courses (
    course_id VarCHAR(10) PRIMARY KEY,
    course_name VARCHAR(255)
)""")

cursor.execute("""CREATE TABLE student_course (
  student_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students (student_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
)""")

with open('students.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO students (student_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3])
        cursor = mydb.cursor()
        cursor.execute(query, values)

with open('courses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = mydb.cursor()
        cursor.execute(query, values)

with open('student_course.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = mydb.cursor()
        cursor.execute(query, values)

mydb.commit()
mydb.close()