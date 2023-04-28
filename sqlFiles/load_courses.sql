LOAD DATA LOCAL INFILE './courses.csv'
               INTO TABLE courses
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (course_id, course_name);