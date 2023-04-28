LOAD DATA LOCAL INFILE './sections.csv'
               INTO TABLE sections
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (section_id, course_id, section_title);