LOAD DATA LOCAL INFILE './admin.csv'
               INTO TABLE admins
               FIELDS TERMINATED BY ',' ENCLOSED BY '"'
               LINES TERMINATED BY '\n'
               IGNORE 1 ROWS
               (admin_id, first_name, last_name, email, password, user_type, account_type);