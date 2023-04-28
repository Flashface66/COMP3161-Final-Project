INSERT INTO users (account_id, first_name, last_name, email, user_type, account_type)
            SELECT admin_id, first_name, last_name, email, user_type, 'admins' FROM admins ;

            INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
            SELECT student_id, first_name, last_name, email, password, user_type, 'students' FROM students;

            INSERT INTO users (account_id, first_name, last_name, email, password, user_type, account_type)
            SELECT lect_id, first_name, last_name, email, password, user_type, 'lecturers' FROM lecturers;
            