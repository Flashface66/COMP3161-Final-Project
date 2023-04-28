LOAD DATA LOCAL INFILE './submissions.csv'
               INTO TABLE submissions
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id, student_id, course_id, file, due_date);