LOAD DATA LOCAL INFILE './assignments.csv'
               INTO TABLE assignments
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id,course_id,assignment_name,due_date);