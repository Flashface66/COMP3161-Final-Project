LOAD DATA LOCAL INFILE './students.csv'
               INTO TABLE student
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '
'
               IGNORE 1 ROWS
               (student_id, first_name, last_name, email, password, user_type, account_type);