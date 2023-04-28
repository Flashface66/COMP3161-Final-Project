import mysql.connector
import os
import csv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)


cursor = db.cursor()
cursor.execute("USE notquiteourvle")
cursor.execute("DROP TABLE IF EXISTS section_content")
cursor.execute("DROP TABLE IF EXISTS sections")




cursor.execute("""CREATE TABLE sections (
    section_id INT AUTO_INCREMENT,
    course_id VARCHAR(50),
    section_title VARCHAR(500),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY(section_id, course_id)
)""")


cursor.execute("""CREATE TABLE section_content (
    content_id INT AUTO_INCREMENT,
    section_id INT,
    course_id VARCHAR(50),
    content_name TEXT,
    content_file TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    PRIMARY KEY(content_id, section_id)
)""")


sectionpath = os.path.join('./csvs', 'sections.csv')
with open(sectionpath, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO sections (section_id, course_id,section_title) VALUES (%s, %s, %s)"
        values = (int(row[0]), row[1], row[2])
        cursor = db.cursor()
        cursor.execute(query, values)


sectcontent = os.path.join('./csvs', 'sectioncontent.csv')
with open(sectcontent, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO section_content (section_id, course_id, content_name,content_file) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3])
        cursor = db.cursor()
        cursor.execute(query, values)

db.commit()
db.close()