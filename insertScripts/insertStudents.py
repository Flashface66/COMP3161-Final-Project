import csv
import mysql.connector
import os
import hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)


cursor = db.cursor()
cursor.execute("USE notquiteourvle")
cursor.execute("DROP TABLE IF EXISTS students")


cursor.execute("""CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT
)""")

studroster = os.path.join('./csvs', 'students.csv')

with open(studroster, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        passhash = hashlib.sha256(row[4].encode()).hexdigest()
        query = "INSERT INTO students (student_id, first_name, last_name, email, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3], passhash, row[5])
        cursor = db.cursor()
        cursor.execute(query, values)



sql_query = """LOAD DATA LOCAL INFILE './students.csv'
               INTO TABLE students
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (student_id, first_name, last_name, email, password, user_type, account_type);"""


studentroster = os.path.join('./sqlFiles', 'load_students.sql')
with open(studentroster, "w") as f:
    f.write(sql_query)



cursor.execute("""
    INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
    SELECT student_id, first_name, last_name, email, password, user_type, 'students' FROM students
""")

db.commit()
db.close()