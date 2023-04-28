import random
import datetime
import csv
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root", password="Passwordnt")
cursor = db.cursor()
cursor.execute("USE notquiteourvle")

file = open("filename.txt", "w")

cursor.execute("SELECT course_id, lect_id FROM lect_course")
records = cursor.fetchall()
courses_dict = {record[1]: record[0] for record in records}

duedates = {
    1: '2023-01-31 23:55:00',
    2: '2023-02-28 23:55:00',
    3: '2023-03-31 23:55:00',
    4: '2023-04-30 23:55:00',
    5: '2023-05-31 23:55:00',
}
startdates = {
    1: '2023-01-01 00:00:00',
    2: '2023-02-01 00:0:00',
    3: '2023-03-01 00:00:00',
    4: '2023-04-01 00:00:00',
    5: '2023-05-01 00:00:00',
}


cursor=db.cursor(dictionary=True)
cursor.execute("SELECT course_id FROM courses")
course_ids = cursor.fetchall()

assignmentrecords = []
for course_id in course_ids:
    for i in range(1,6):
        
        name= "ASSIGNMENT " + str(i)
        submitted = str(duedates[i])

        assignmentrecords.append([i, course_id["course_id"], name, submitted])


with open('assignments.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['assignment_id', 'course_id', 'assignment_name', 'due_date'])
    for assignment in assignmentrecords:
        writer.writerow(assignment)

cursor=db.cursor(dictionary=False)
cursor.execute("SELECT * FROM student_course")
student_courses = cursor.fetchall()


submissions = []
grades = []

for student_course in student_courses:
    student_id = student_course[0]
    course_id = student_course[1]

    random_dates = {}

    for key in duedates:
        startdate = datetime.datetime.strptime(startdates[key], '%Y-%m-%d %H:%M:%S')
        duedate = datetime.datetime.strptime(duedates[key], '%Y-%m-%d %H:%M:%S')
        random_date = startdate + (duedate - startdate) * random.random()
        random_dates[key] = random_date.strftime('%Y-%m-%d %H:%M:%S')
    
    for x in range(1,6):
        grade = round(random.uniform(0.00, 100.00), 2)
        filename= str(student_id) + "_" + course_id + "_Assignment_" + str(x) + ".doc"

        submissions.append([x, student_id, course_id, filename, random_dates[x]])
        grades.append([student_id, course_id, grade, x])

with open('submissions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['assignment_id', 'student_id', 'course_id', 'file', 'due_date'])
    for records in submissions:
        writer.writerow(records)

with open('grades.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['student_id', 'course_id', 'grade', 'assignment_id'])
    for score in grades:
        writer.writerow(score)




with open('submissions.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        query =  "INSERT INTO submissions (assignment_id, student_id, course_id, file, due_date) VALUES (%s, %s, %s, %s, %s)"
        values = (int(row[0]), int(row[1]), row[2], row[3], row[4])
        cursor = db.cursor()
        cursor.execute(query, values)


with open('grades.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO grades (student_id, course_id, grade, assignment_id) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], int(row[3]))
        cursor = db.cursor()
        cursor.execute(query, values)

with open('assignments.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)

    for row in reader:
        query = "INSERT INTO assignments (assignment_id,course_id,assignment_name,due_date) VALUES (%s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3])
        cursor = db.cursor()
        cursor.execute(query, values)

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()
