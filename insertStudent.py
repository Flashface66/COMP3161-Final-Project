import csv
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root", password="Passwordnt")

cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS notquiteourvle")
cursor.execute("CREATE DATABASE notquiteourvle")
cursor.execute("USE notquiteourvle")

cursor.execute("""CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    user_type INT
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

cursor.execute("""CREATE TABLE lecturers (
    lect_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    user_type INT
)""")

cursor.execute("""CREATE TABLE lect_course (
  lect_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (lect_id, course_id),
  FOREIGN KEY (lect_id) REFERENCES lecturers (lect_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
)""")


cursor.execute("""CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    user_type INT,
    account_type VARCHAR(20)
)""")

cursor.execute("""CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    user_type INT
)""")


cursor.execute("""CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id VARCHAR(50),
    section_name VARCHAR(500),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)""")

cursor.execute("""CREATE TABLE sectionfiles (
    course_id VARCHAR(50),
    section_id INT,
    files VARCHAR(500),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
)""")

cursor.execute("""CREATE TABLE submissions (
    student_id INT,
    assignment_id INT,
    course_id VARCHAR(50),
    file VARCHAR(255),
    due_date DateTime,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    PRIMARY KEY (assignment_id, student_id, course_id),
    INDEX (assignment_id)
)""")

cursor.execute("""CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT,
    course_id VARCHAR(50),
    assignment_name VARCHAR(50),
    due_date DATETIME,
    PRIMARY KEY (assignment_id, course_id)
)""")

cursor.execute("""CREATE TABLE grades (
    student_id INT,
    course_id VARCHAR(50),
    grade DECIMAL(5,2) NOT NULL CHECK (grade >= 0 AND grade <= 100),
    assignment_id INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (assignment_id) REFERENCES submissions(assignment_id)
    PRIMARY KEY(student_id, assignment_id, course_id)

)""")





with open('students.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO students (student_id, first_name, last_name, email, user_type) VALUES (%s, %s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3], row[4])
        cursor = db.cursor()
        cursor.execute(query, values)

with open('lecturers.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO lecturers (lect_id, first_name, last_name, email, user_type) VALUES (%s, %s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3], row[4])
        cursor = db.cursor()
        cursor.execute(query, values)

with open('admin.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO admins (admin_id, first_name, last_name, email, user_type) VALUES (%s, %s, %s, %s,%s)"
        values = (row[0], row[1], row[2], row[3], row[4])
        cursor = db.cursor()
        cursor.execute(query, values)        

with open('courses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)

with open('student_course.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)

with open('lecturer_course.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO lect_course (lect_id, course_id) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)

cursor.execute("""
    INSERT INTO users (account_id, first_name, last_name, email, user_type, account_type)
    SELECT student_id, first_name, last_name, email, user_type, 'students' FROM students
""")

cursor.execute("""
    INSERT INTO users (account_id, first_name, last_name, email, user_type, account_type)
    SELECT lect_id, first_name, last_name, email, user_type, 'lecturers' FROM lecturers 
""")

cursor.execute("""
    INSERT INTO users (account_id, first_name, last_name, email, user_type, account_type)
    SELECT admin_id, first_name, last_name, email, user_type, 'admins' FROM admins 
""")



db.commit()
db.close()