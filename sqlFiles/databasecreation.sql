
CREATE DATABASE notquite_ourvle;

USE notquite_ourvle;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT
);

CREATE TABLE courses (
    course_id VarCHAR(10) PRIMARY KEY,
    course_name VARCHAR(255)
);

CREATE TABLE student_course (
  student_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students (student_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

CREATE TABLE lecturers (
    lect_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT
);

CREATE TABLE lect_course (
  lect_id INT,
  course_id VARCHAR(10),
  PRIMARY KEY (lect_id, course_id),
  FOREIGN KEY (lect_id) REFERENCES lecturers (lect_id),
  FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    user_type INT,
    account_type VARCHAR(20)
);

CREATE TABLE submissions (
    student_id INT,
    assignment_id INT,
    course_id VARCHAR(50),
    file VARCHAR(255),
    due_date DateTime,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    PRIMARY KEY (student_id, assignment_id, course_id),
    INDEX (assignment_id)
);

CREATE TABLE assignments (
    assignment_id INT AUTO_INCREMENT,
    course_id VARCHAR(50),
    assignment_name VARCHAR(50),
    due_date DATETIME,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (assignment_id, course_id)
    
);
CREATE INDEX idx_assignment_id ON assignments (assignment_id);


CREATE TABLE grades (
    student_id INT,
    course_id VARCHAR(50),
    grade DECIMAL(5,2) NOT NULL CHECK (grade >= 0 AND grade <= 100),
    assignment_id INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (assignment_id) REFERENCES submissions(assignment_id),
    PRIMARY KEY(student_id, assignment_id, course_id)
); 

CREATE TABLE calendar_events (
    event_id INT AUTO_INCREMENT NOT NULL,
    assignment_id INT NULL,
    course_id VARCHAR(50),
    event_name VARCHAR (500),
    due_date DATETIME,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
    PRIMARY KEY (event_id)
);

CREATE TABLE forums (
    forum_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(50),
    forum_name VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE discussion_threads (
    thread_id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT,
    student_id INT,
    thread_title VARCHAR(255),
    thread_post TEXT,
    parent_thread_id INT DEFAULT NULL,
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (parent_thread_id) REFERENCES discussion_threads(thread_id) ON DELETE CASCADE
);

CREATE INDEX idx_forum_id ON discussion_threads(forum_id);

CREATE TABLE sections (
    section_id INT AUTO_INCREMENT,
    course_id VARCHAR(50),
    section_title VARCHAR(500),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY(section_id, course_id)
);


CREATE TABLE section_content (
    content_id INT AUTO_INCREMENT,
    section_id INT,
    course_id VARCHAR(50),
    content_name TEXT,
    content_file TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    PRIMARY KEY(content_id, section_id)
);


