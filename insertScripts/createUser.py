import csv
import os
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)


cursor = db.cursor()
cursor.execute("USE notquiteourvle")
cursor.execute("DROP TABLE IF EXISTS users")


cursor.execute("""CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT,
    account_type VARCHAR(20)
)""")


sql_query = """INSERT INTO users (account_id, first_name, last_name, email, user_type, account_type)
            SELECT admin_id, first_name, last_name, email, user_type, 'admins' FROM admins ;

            INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
            SELECT student_id, first_name, last_name, email, password, user_type, 'students' FROM students;

            INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
            SELECT lect_id, first_name, last_name, email, password, user_type, 'lecturers' FROM lecturers;
            """


importusers = os.path.join('./sqlFiles', 'load_users.sql')
with open(importusers, "w") as f:
    f.write(sql_query)

db.commit()
db.close()