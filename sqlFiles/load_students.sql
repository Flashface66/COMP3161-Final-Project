LOAD DATA LOCAL INFILE './students.csv'
               INTO TABLE students
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (student_id, first_name, last_name, email, password, user_type, account_type);