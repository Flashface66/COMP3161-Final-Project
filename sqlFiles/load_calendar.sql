LOAD DATA LOCAL INFILE './calendarevents.csv'
               INTO TABLE calendar_events
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (assignment_id, course_id, event_name, due_date);