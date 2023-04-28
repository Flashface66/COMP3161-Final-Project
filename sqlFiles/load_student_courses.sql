LOAD DATA LOCAL INFILE './student_courses.csv'
               INTO TABLE student_course
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '
'
               IGNORE 1 ROWS
               (student_id, course_id);