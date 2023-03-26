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
    email VARCHAR(100),
    course_id VARCHAR(255)
)""")

with open('students.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO students (student_id, first_name, last_name, email, course_id) VALUES (%s, %s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3], row[4])
        cursor = mydb.cursor()
        cursor.execute(query, values)

mydb.commit()
mydb.close()