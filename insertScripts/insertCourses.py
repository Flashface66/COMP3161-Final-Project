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
cursor.execute("DROP TABLE IF EXISTS courses")


cursor.execute("""CREATE TABLE courses (
    course_id VarCHAR(10) PRIMARY KEY,
    course_name VARCHAR(255)
)""")


courses = os.path.join('./csvs', 'courses.csv')

with open(courses, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query = "INSERT INTO courses (course_id, course_name) VALUES (%s, %s)"
        values = (row[0], row[1])
        cursor = db.cursor()
        cursor.execute(query, values)

sql_query = """LOAD DATA LOCAL INFILE './courses.csv'
               INTO TABLE courses
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (course_id, course_name);"""


allcourses = os.path.join('./sqlFiles', 'load_courses.sql')
with open(allcourses, "w") as f:
    f.write(sql_query)


db.commit()
db.close()