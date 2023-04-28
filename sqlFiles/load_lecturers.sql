LOAD DATA LOCAL INFILE './lecturers.csv'
               INTO TABLE lecturers
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (lect_id, first_name, last_name, email, password, user_type, account_type);