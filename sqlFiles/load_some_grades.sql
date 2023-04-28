LOAD DATA LOCAL INFILE './grades.csv'
               INTO TABLE grades
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (student_id, course_id, grade, assignment_id);