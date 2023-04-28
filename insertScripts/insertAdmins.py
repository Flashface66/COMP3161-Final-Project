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
cursor.execute("DROP TABLE IF EXISTS admins")


cursor.execute("""CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT
)""")

adminroster = os.path.join('./csvs', 'admin.csv')

with open(adminroster, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    
    for row in reader:
        passhash = hashlib.sha256(row[4].encode()).hexdigest()
        query = "INSERT INTO admins (admin_id, first_name, last_name, email, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (int(row[0]), row[1], row[2], row[3], passhash, row[5])
        cursor = db.cursor()
        cursor.execute(query, values)

cursor.execute("""
    INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
    SELECT admin_id, first_name, last_name, email, password, user_type, 'admins' FROM admins
""")

sql_query = """LOAD DATA LOCAL INFILE './admin.csv'
               INTO TABLE admins
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (admin_id, first_name, last_name, email, password, user_type, account_type);"""


alladmin = os.path.join('./sqlFiles', 'load_admins.sql')
with open(alladmin, "w") as f:
    f.write(sql_query)


db.commit()
db.close()