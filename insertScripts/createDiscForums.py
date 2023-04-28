import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt"
)


cursor = db.cursor()
cursor.execute("USE notquiteourvle")
cursor.execute("DROP TABLE IF EXISTS forums")
cursor.execute("DROP TABLE IF EXISTS discussion_threads")


cursor.execute("""CREATE TABLE forums (
    forum_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(50),
    forum_name VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
)""")

cursor.execute("""CREATE TABLE discussion_threads (
    thread_id INT PRIMARY KEY AUTO_INCREMENT,
    forum_id INT,
    student_id INT,
    thread_title VARCHAR(255),
    thread_post TEXT,
    parent_thread_id INT DEFAULT NULL,
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (parent_thread_id) REFERENCES discussion_threads(thread_id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE INDEX idx_forum_id ON discussion_threads(forum_id)""")

db.commit()
db.close()