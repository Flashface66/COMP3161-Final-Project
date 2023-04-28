LOAD DATA LOCAL INFILE './lecturer_course.csv'
               INTO TABLE lect_course
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '
'
               IGNORE 1 ROWS
               (lect_id, course_id);