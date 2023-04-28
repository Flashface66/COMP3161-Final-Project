LOAD DATA LOCAL INFILE './sectioncontent.csv'
               INTO TABLE section_content
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (section_id, course_id, content_name, content_file);