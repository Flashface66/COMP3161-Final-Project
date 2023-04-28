"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from datetime import datetime
import hashlib
from flask_login import login_user, logout_user, current_user, login_required

from app import app, login_manager, db
from flask import flash, jsonify, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
 
from app.forms import *
import mysql.connector
from flask_login import UserMixin


###
# Routing for your application.
###

@app.route('/')
@login_required
def home():
    """Render website's home page."""
    
    cursor = db.cursor(dictionary=True)
    
    # Fetch all courses for the specified student
    select_courses_query = """
        SELECT c.course_id, c.course_name
        FROM courses c
        INNER JOIN student_course sc ON c.course_id = sc.course_id
        WHERE sc.student_id = %s;
    """.format()
    cursor.execute(select_courses_query, (current_user.id,))
    courses = cursor.fetchall()
    print(courses)

    # Loop through each course and fetch its sections and content
    content = []
    for course in courses:
        select_sections_query = """
            SELECT s.section_id, s.section_title, sc.content_id, sc.content_name, sc.content_file
            FROM sections s
            INNER JOIN section_content sc ON s.section_id = sc.section_id AND s.course_id = sc.course_id
            WHERE s.course_id = %s;
        """
        cursor.execute(select_sections_query, (course['course_id'],))
        sections = cursor.fetchall()

        # Create a dictionary to group section content by section title
        section_content_dict = {}
        for section in sections:
            section_title = section['section_title']
            if section_title not in section_content_dict:
                section_content_dict[section_title] = []
            section_content_dict[section_title].append({
                'content_id': section['content_id'],
                'content_name': section['content_name'],
                'content_file': section['content_file']
            })

        # Create a list of sections with their content grouped by section title
        grouped_sections = []
        for section_title, section_content in section_content_dict.items():
            grouped_sections.append({
                'section_title': section_title,
                'section_content': section_content
            })

        course_content = {
            'course_id': course['course_id'],
            'course_name': course['course_name'],
            'sections': grouped_sections
        }
        content.append(course_content)


    return render_template('home.html', content=content, courses=courses)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self._is_active = True

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Authenticate user login."""
    

    form = LoginForm()
    # Get the username and password values from the request.
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Get the username and password from the JSON data
        username = request.json.get('username')
        password = request.json.get('password')
    else :
        # Get the username and password from the form data
        username = request.form.get('username')
        password = request.form.get('password')
    

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (username,))
    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data)

    if user_data is not None and (hashlib.sha256(password.encode()).hexdigest() == user_data["password"]):
        user = User(user_data['account_id'])
        login_user(user)
        if request.is_json:
            return jsonify({'message': 'Logged in successfully.'}), 200
        else:
            flash('Logged in successfully.')
            return redirect(url_for('home'))
    else:
        if request.is_json:
            print(request.is_json)
            return jsonify({'message': 'Invalid user ID'}), 401
        else:
            flash('Invalid user ID or user type.')
            return render_template('login.html', form=form)
        


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render website's registration page."""
    
    
    form = RegisterStudentForm()
    # Get the username and password values from the request.
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json' and not None:
        # Get the username and password from the JSON data
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        user_type = request.json.get('user_type')
        password = request.json.get('password')
    else :
        # Get the username and password from the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_type = request.form.get('user_type')
        password = request.form.get('password')

    if all([first_name, last_name, user_type, password]):
        # Get the form data submitted by the user
       
        if user_type == '1':
            db_table = 'students'
            

        elif user_type == '2':
            db_table = 'lecturers'

        
        
        email = str(last_name + "."+ first_name + "@example.com")
        cursor = db.cursor()
        query = "INSERT INTO notquiteourvle.{} (first_name, last_name, email, user_type, password) VALUES (%s, %s, %s, %s, %s)".format(db_table)
        print(query)
        values = (first_name, last_name, email, user_type,hashlib.sha256(password.encode()).hexdigest())
        cursor.execute(query, values)

     
        user_id = cursor.lastrowid
        user_query = "INSERT INTO notquiteourvle.users (account_id,first_name, last_name, email, user_type, account_type, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        print(user_query)
        values = ( user_id, first_name, last_name, email, user_type, db_table, hashlib.sha256(password.encode()).hexdigest())
        cursor.execute(user_query, values)
        db.commit()

        if request.is_json:
            return jsonify({'message': 'User created successfully.'}), 200
        else:
            flash(f'You have successfully registered with student ID: {user_id}.', 'success')
            user = User(user_id)
            login_user(user)
            return redirect(url_for('home'))
        

    return render_template('register.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



@app.route('/courses', methods=["GET"])
@login_required
def courses():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
        )
    cursor = db.cursor(dictionary=True)
    course_query = "SELECT * FROM notquiteourvle.courses"
    cursor.execute(course_query)
    courses = cursor.fetchall()
    print(request.is_json)
    if request.is_json:
        return jsonify(courses)
    else:
        return render_template('courses.html',  courses=courses)
   

@app.route('/students')
@login_required
def students():
    """Render student's my course page."""
    
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.students "
    cursor.execute(student_query)
    students = cursor.fetchall()

    

    if request.is_json:
        return jsonify(students)
    else:
        return render_template('students.html', students=students)
 


@app.route('/lecturers')
@login_required
def lecturers():
    """Render student's my course page."""
    
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    lecturer_query = "SELECT * FROM notquiteourvle.lecturers "
    cursor.execute(lecturer_query)
    lecturers = cursor.fetchall()

    if request.is_json:
        return jsonify(lecturers)
    else:
        return render_template("lecturers.html", lecturers=lecturers)



@app.route('/<course_id>/members')
@login_required
def course_members(course_id):
    """Render course members page."""
    
    cursor = db.cursor(dictionary=True)

    # Retrieve the lecturers for the given course ID
    lecturer_query = """
        SELECT lecturers.lect_id, lecturers.first_name, lecturers.last_name
        FROM notquiteourvle.lecturers
        JOIN lect_course ON lecturers.lect_id = lect_course.lect_id
        WHERE lect_course.course_id = %s;
     """
    cursor.execute(lecturer_query, (course_id,))
    lecturers = cursor.fetchall()

    # Retrieve the students for the given course ID
    student_query = """
        SELECT students.student_id, students.first_name, students.last_name
        FROM notquiteourvle.students
        JOIN student_course ON students.student_id = student_course.student_id
        WHERE student_course.course_id = %s;
     """
    cursor.execute(student_query, (course_id,))
    students = cursor.fetchall()

    if request.is_json:
        members = {"lecturers": lecturers, "students": students}
        return jsonify(members)
    else:
        return render_template("course_members.html", lecturers=lecturers, students=students)

   

@app.route('/<user_id>/courses')
@login_required
def user_courses(user_id):
    """Render user's courses page."""
    
    cursor = db.cursor(dictionary=True)

   
    # Retrieve the user's information
    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    print(user)

    if user["user_type"] == 1:  # student
        # Retrieve the courses for the given student ID
        course_query = """
            SELECT courses.*
            FROM courses
            JOIN student_course ON courses.course_id = student_course.course_id
            WHERE student_course.student_id = %s
        """
        cursor.execute(course_query, (user["account_id"],))
        courses = cursor.fetchall()
    elif user["user_type"] == 2:  # lecturer
        # Retrieve the courses for the given lecturer ID
        course_query = """
            SELECT courses.*
            FROM courses
            JOIN lect_course ON courses.course_id = lect_course.course_id
            WHERE lect_course.lect_id = %s
        """
        cursor.execute(course_query, (user["account_id"],))
        courses = cursor.fetchall()
    else:
        courses = []

    if request.is_json:
        return jsonify(courses)
    else:
        return render_template("user_course.html", courses=courses)




@app.context_processor
def inject_user():
    """Pass the user object to all templates."""
    if current_user.is_authenticated:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Passwordnt",
            database="notquiteourvle"
        )
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM notquiteourvle.users WHERE account_id = %s"

        cursor.execute(query, (current_user.id,))
        user = cursor.fetchone()
        
        return dict(user=user)
    else:
        return dict(user={})
        
    
  
@app.route('/<student_id>/student/course/registration' ,methods=["PUT"])
@login_required
def student_registration(student_id):
    
    cursor = db.cursor(dictionary=True)
    content = request.json
    course_id = content["course_id"]
    query="INSERT INTO notquiteourvle.student_course (student_id,course_id) VALUES (%s, %s)"
    values = (student_id, course_id)

    cursor.execute(query, values)
    db.commit()
    return jsonify(values)


@app.route('/<lect_id>/lecturer/course/registration', methods=["PUT"])
@login_required
def lecturer_registration(lect_id):
    
    cursor = db.cursor(dictionary=True)
    content = request.json
    course_id = content["course_id"]
    query = '''
                SELECT * FROM notquiteourvle.lect_course WHERE course_id = %s;
            '''

    cursor.execute(query, (course_id,))
    result = cursor.fetchone()

    if result:
        # If course ID already exists, update the lecturer ID for that course
        delete_query='''
                    DELETE FROM notquiteourvle.lect_course WHERE course_id = %s;

                    '''

        insert_query = '''
                            INSERT INTO notquiteourvle.lect_course (lect_id, course_id) VALUES (%s, %s);
                        '''
        
        cursor.execute(delete_query, (course_id,))
        cursor.execute(insert_query, (lect_id, course_id))
    else:
        # If course ID does not exist, insert a new row
        insert_query = '''
                            INSERT INTO notquiteourvle.lect_course (lect_id, course_id) VALUES (%s, %s);
                        '''
        cursor.execute(insert_query, (lect_id, course_id))

    db.commit()
    return jsonify({"lect_id": lect_id, "course_id": course_id})

@app.route('/courses/create', methods=["PUT"])
@login_required
def create_course():

    cursor = db.cursor(dictionary=True)
    content = request.json
    course_id = content["course_id"]
    course_name = content["course_name"]
    

    
    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data['user_type'])

    if user_data['user_type'] == 3:
        insert_query='INSERT INTO notquiteourvle.courses (course_id, course_name) VALUES (%s, %s); '
        cursor.execute(insert_query, (course_id, course_name))
        db.commit()

        return jsonify({"course_id":course_id,"course_name":course_name})
    else:
        return jsonify({"message":'Wrong access level'})
    


@app.route('/<course_id>/assignments')
@login_required
def get_assignments(course_id):
    cursor = db.cursor(dictionary=True)
    query = 'SELECT * FROM notquiteourvle.assignments WHERE course_id=%s '
    cursor.execute(query, (course_id,))
    assignments = cursor.fetchall()
    if request.is_json:
        return jsonify(assignments)
    else:
        return render_template("user_course.html", courses=courses)
    

@app.route('/<student_id>/<course_id>/grades')
@login_required
def get_course_grades(course_id,student_id):
    cursor = db.cursor(dictionary=True)
    query = 'SELECT * FROM notquiteourvle.grades WHERE course_id=%s and student_id=%s '
    cursor.execute(query, (course_id,student_id,))
    grades = cursor.fetchall()
    if request.is_json:
        return jsonify(grades)
    else:
        return render_template("user_course.html", courses=courses)
    

@app.route('/<student_id>/grades')
@login_required
def get_student_grades(student_id):
    cursor = db.cursor(dictionary=True)
    query = 'SELECT * FROM notquiteourvle.grades WHERE student_id=%s '
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()
    print(grades)
    if request.is_json:
        grades_by_course = {}
        for grade in grades:
            course_code = grade['course_id']
            if course_code not in grades_by_course:
                grades_by_course[course_code] = []
            grades_by_course[course_code].append(grade)
        
        # Convert the grouped grades to JSON
        return jsonify(grades_by_course)
    else:
        return render_template("grades.html", grades=grades)    


@app.route('/<student_id>/final_average')
@login_required
def get_student_average(student_id):
    cursor = db.cursor(dictionary=True)
    query = 'SELECT course_id, ROUND(AVG(grade),2) as avg_grade FROM notquiteourvle.grades WHERE student_id=%s GROUP BY course_id '
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()

    query = '''
            SELECT ROUND(AVG(avg_grade),2) AS final_avg 
                FROM (
                    SELECT AVG(grade) AS avg_grade 
                    FROM notquiteourvle.grades 
                    WHERE student_id=%s 
                    GROUP BY course_id
                ) AS course_avgs;
            '''
    cursor.execute(query, (student_id,))
    final_avg = cursor.fetchone()
    if request.is_json:
        return jsonify({"Final Average" : final_avg, "Course Averages" : grades})
    else:
        return render_template("grades.html", grades=grades) 


    
     
@app.route('/<course_id>/assignment/create', methods=["PUT"])
@login_required
def create_assignment(course_id):
    cursor = db.cursor(dictionary=True)
    content = request.json  
    assignment_name = content["assignment_name"]
    due_date = content["due_date"]

    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    

    print(user_data['user_type'])

    if user_data['user_type'] == 2:
        select_assignment_id_query = """
            SELECT assignment_id FROM notquiteourvle.assignments WHERE course_id = %s ORDER BY assignment_id DESC LIMIT 1;

        """

        cursor.execute(select_assignment_id_query, (course_id,))
        # print(cursor.fetchone())
        assignment_id = (cursor.fetchone())
        print(assignment_id["assignment_id"])
        new_id=(assignment_id["assignment_id"])+1

        insert_assignment_query = """
            INSERT INTO notquiteourvle.assignments (assignment_id, course_id, assignment_name, due_date)
            VALUES (%s, %s, %s, %s);
        """

        cursor.execute(insert_assignment_query, (new_id, course_id, assignment_name, due_date))

        

        # Create a new row in the calendar_events table for the new assignment
        insert_calendar_query = "INSERT INTO notquiteourvle.calendar_events (assignment_id, course_id, event_name, due_date) VALUES (%s, %s, %s, %s);"
        event_name = f"Assignment: {assignment_name}"
        cursor.execute(insert_calendar_query, (new_id, course_id, event_name, due_date))
        db.commit()

        return jsonify({"course_id":course_id,"assignment_name":assignment_name,"due_date":due_date})
    else:
        return jsonify({"message":'Wrong access level'})




@app.route('/<int:student_id>/<string:course_id>/<int:assignment_id>/submission', methods=['PUT'])
@login_required
def submit_assignment(student_id, course_id, assignment_id):
    
    # Check if file was uploaded
    form = SubmissionForm()
    
    if request.is_json:
        # Get the username and password from the JSON data
        content = request.json  
        file=content["file"]
        filename = file
    else :
        # Get the username and password from the form data
        
        file = request.form.get('assignment')
        filename = secure_filename(file.filename)
    
    # Save file to server
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data['user_type'])
    # Insert submission into database
    if user_data['user_type'] == 1:
        cursor = db.cursor()
        due_date = datetime.now()
        query = "INSERT INTO submissions (student_id, course_id, assignment_id, file, due_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (student_id, course_id, assignment_id, filename, due_date))
        db.commit()
        return 'Assignment submitted successfully.', 200
    else:
        return jsonify({"message":'Wrong access level'})
    
    
@app.route('/<int:student_id>/<string:course_id>/<int:assignment_id>/grade', methods=['PUT'])
@login_required
def submit_grade(student_id, course_id, assignment_id):
    # Check if file was uploaded
    
    if request.is_json:
        # Get the username and password from the JSON data
        content = request.json  
        grade=content["grade"]
        
    else :
        # Get the username and password from the form data
        file = request.form.get('assignment')
        filename = secure_filename(file.filename)
        
    # Save file to server
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data['user_type'])
    # Insert submission into database
    if user_data['user_type'] == 2:
        cursor = db.cursor()
        query = "INSERT INTO grades (student_id, course_id, assignment_id, grade) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (student_id, course_id, assignment_id, grade))
        db.commit()
        return jsonify({"student_id": student_id, "course_id": course_id, "assignment_id": assignment_id, "grade": grade})
    else:
        return jsonify({"message":'Wrong access level'})
    





@app.route('/courses/<string:course_id>/calendar_events', methods=['PUT'])
def create_calendar_event(course_id):
    # Get data from the POST request
    data = request.get_json()


    # Create a new calendar event
    cursor = db.cursor()
    query = """
        INSERT INTO calendar_events (assignment_id, course_id, event_name, due_date)
        VALUES (%s, %s, %s, %s)
    """
    values = (data.get("assignment_id"), course_id, data['event_name'], data['due_date'])
    cursor.execute(query, values)
    db.commit()

    # Close the database connection
    cursor.close()
    db.close()

    # Return a success message
    return jsonify({'message': 'Calendar event created successfully.'}), 201



@app.route('/calendar_events/<course_id>')
def get_calendar_events(course_id):
    try:
        with db.cursor() as cursor:
            sql = """
                SELECT event_id, event_name, due_date
                FROM calendar_events
                WHERE course_id = %s
            """
            cursor.execute(sql, (course_id,))
            result = cursor.fetchall()
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/<course_id>/forum/create', methods=["PUT"])
@login_required
def create_forum(course_id):
    cursor = db.cursor(dictionary=True)
    content = request.json  
    forum_name = content["forum_name"]

   
    insert_query='INSERT INTO notquiteourvle.forums (course_id, forum_name) VALUES (%s, %s);'
    cursor.execute(insert_query, (course_id, forum_name))
    db.commit()

    return jsonify({"course_id":course_id,"forum_name":forum_name})




@app.route('/forums/<forum_id>/threads', methods=["PUT"])
@login_required
def create_thread(forum_id):
    cursor = db.cursor(dictionary=True)
    content = request.json  
    thread_title = content["thread_title"]
    thread_post = content["thread_post"]
    parent_thread_id = content.get("parent_thread_id")
    student_id = content["student_id"]

    # # Check if the user is enrolled in the course associated with the forum
    # query = "SELECT * FROM notquiteourvle.students WHERE student_id=%s AND course_id=(SELECT course_id FROM notquiteourvle.forums WHERE forum_id=%s)"
    # cursor.execute(query, (student_id, forum_id))
    # results = cursor.fetchall()
    # if not results:
    #     return jsonify({"message":'User is not enrolled in the course.'})

    # Insert the new thread into the database
    insert_query='INSERT INTO notquiteourvle.discussion_threads (forum_id, student_id, thread_title, thread_post, parent_thread_id) VALUES (%s, %s, %s, %s, %s); '
    cursor.execute(insert_query, (forum_id, student_id, thread_title, thread_post, parent_thread_id))
    thread_id = cursor.lastrowid
    db.commit()

    # Get the newly created thread and return it as a response
    select_query = "SELECT * FROM notquiteourvle.discussion_threads WHERE thread_id=%s"
    cursor.execute(select_query, (thread_id,))
    result = cursor.fetchone()

    return jsonify(result)



@app.route('/<course_id>/sections', methods=["GET"])
@login_required
def sections(course_id):
    cursor = db.cursor(dictionary=True)

    select_sections_query = """
        SELECT * FROM notquiteourvle.sections WHERE course_id = %s;
    """
    cursor.execute(select_sections_query, (course_id,))
    sections = cursor.fetchall()

    return jsonify({"sections": sections})




@app.route('/<course_id>/section/create', methods=["PUT"])
@login_required
def create_section(course_id):
    cursor = db.cursor(dictionary=True)
    content = request.json  
    section_title = content["section_title"]




    select_section_id_query = """
            SELECT section_id FROM notquiteourvle.sections WHERE course_id = %s ORDER BY section_id DESC LIMIT 1;

        """

    cursor.execute(select_section_id_query, (course_id,))
    # print(cursor.fetchone())
    section_id = (cursor.fetchone())
    print(section_id["section_id"])
    new_id=(section_id["section_id"])+1


    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data['user_type'])

    if user_data['user_type'] == 2:
        insert_assignment_query='INSERT INTO notquiteourvle.sections (section_id,course_id, section_title) VALUES (%s, %s, %s); '
        cursor.execute(insert_assignment_query, (new_id, course_id, section_title))
        db.commit()

        return jsonify({"course_id":course_id,"section_title":section_title})
    else:
        return jsonify({"message":'Wrong access level'})


@app.route('/<course_id>/content')
def view_section_content(course_id):
    cursor = db.cursor(dictionary=True)
    
    # Fetch all sections for the specified course
    select_sections_query = """
        SELECT * FROM notquiteourvle.sections WHERE course_id = %s;
    """
    cursor.execute(select_sections_query, (course_id,))
    sections = cursor.fetchall()
    
    # Loop through each section and fetch its content
    content = []
    for section in sections:
        select_content_query = """
            SELECT * FROM notquiteourvle.section_content WHERE course_id = %s AND section_id = %s;
        """
        cursor.execute(select_content_query, (course_id, section['section_id']))
        section_content = cursor.fetchall()
        content.append(section_content)

    if request.is_json:
        return jsonify({"sections":sections, "content":content})
    else:
        template1 = render_template('home.html', sections=sections, content=content)
        template2 = render_template('sections.html', sections=sections, content=content)

        return template1, template2






@app.route('/<course_id>/<section_id>/create', methods=["PUT"])
@login_required
def create_section_content(course_id,section_id):
    cursor = db.cursor(dictionary=True)
    content = request.json 
    content_name = content["content_name"]
    content_file = content["content_file"]




    select_content_id_query = """
            SELECT content_id FROM notquiteourvle.section_content WHERE course_id = %s ORDER BY content_id DESC LIMIT 1;

        """

    cursor.execute(select_content_id_query, (course_id,))
    # print(cursor.fetchone())
    content_id = (cursor.fetchone())
    print(content_id["content_id"])
    new_id=(content_id["content_id"])+1


    query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
    cursor.execute(query, (current_user.id,))

    print(cursor)
    results = cursor.fetchall()
    user_data = results[0] if results else None

    print(user_data['user_type'])

    if user_data['user_type'] == 2:
        insert_query='INSERT INTO notquiteourvle.section_content (content_id, section_id, course_id, content_name, content_file) VALUES (%s, %s, %s, %s, %s); '
        cursor.execute(insert_query, (new_id, section_id, course_id, content_name, content_file))
        db.commit()

        return jsonify({"section_id":new_id, "course_id":course_id, "content_name":content_name, "content_file":content_file})
    else:
        return jsonify({"message":'Wrong access level'})


@app.route('/courses_with_50_students_or_more', methods=['GET'])
def courses_with_50_students_or_more():
 
    try:
        # Create the view
        with db.cursor() as cursor:
            cursor.execute('CREATE OR REPLACE VIEW courses_with_50_students_or_more AS '
                           'SELECT c.course_id, c.course_name, COUNT(sc.student_id) AS num_students '
                           'FROM courses c '
                           'JOIN student_course sc ON c.course_id = sc.course_id '
                           'GROUP BY c.course_id '
                           'HAVING num_students >= 50')
        
        # Query the view and return the results as JSON
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM courses_with_50_students_or_more')
            result = cursor.fetchall()
            
            # Convert the result to a list of dictionaries
            courses = []
            for row in result:
                course = {
                    'course_id': row[0],
                    'course_name': row[1],
                    'num_students': row[2]
                }
                courses.append(course)
            
            # Return the courses as JSON
            return jsonify(courses)
    
    finally:
        db.commit()

@app.route('/students_with_5_or_more_courses', methods=['GET'])
def students_with_5_or_more_courses():

    try:
        # Create the view
        with db.cursor() as cursor:
            cursor.execute('CREATE OR REPLACE VIEW students_with_5_or_more_courses AS '
                           'SELECT s.student_id, s.first_name, s.last_name, COUNT(sc.course_id) AS num_courses '
                           'FROM students s '
                           'JOIN student_course sc ON s.student_id = sc.student_id '
                           'GROUP BY s.student_id '
                           'HAVING num_courses >= 5')
        
        # Query the view and return the results as JSON
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM students_with_5_or_more_courses')
            result = cursor.fetchall()
            
            # Convert the result to a list of dictionaries
            students = []
            for row in result:
                student = {
                    'student_id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'num_courses': row[3]
                }
                students.append(student)
            
            # Return the students as JSON
            return jsonify(students)
    
    finally:
        db.commit()

@app.route('/lecturers_with_3_or_more_courses', methods=['GET'])
def lecturers_with_3_or_more_courses():

    try:
        # Create the view
        with db.cursor() as cursor:
            cursor.execute('CREATE OR REPLACE VIEW lecturers_with_3_or_more_courses AS '
                           'SELECT l.lect_id, l.first_name, l.last_name, COUNT(lc.course_id) AS num_courses '
                           'FROM lecturers l '
                           'JOIN lect_course lc ON l.lect_id = lc.lect_id '
                           'GROUP BY l.lect_id '
                           'HAVING num_courses >= 3')
        
        # Query the view and return the results as JSON
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM lecturers_with_3_or_more_courses')
            result = cursor.fetchall()
            
            # Convert the result to a list of dictionaries
            lecturers = []
            for row in result:
                lecturer = {
                    'lect_id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'num_courses': row[3]
                }
                lecturers.append(lecturer)
            
            # Return the lecturers as JSON
            return jsonify(lecturers)
    
    finally:
        db.commit()

@app.route('/top_10_enrolled_courses', methods=['GET'])
def top_10_enrolled_courses():
    try:
        # Create the view
        with db.cursor() as cursor:
            cursor.execute('CREATE OR REPLACE VIEW top_10_enrolled_courses AS '
                           'SELECT c.course_id, c.course_name, COUNT(sc.student_id) AS num_students '
                           'FROM courses c '
                           'JOIN student_course sc ON c.course_id = sc.course_id '
                           'GROUP BY c.course_id '
                           'ORDER BY num_students DESC '
                           'LIMIT 10')
        
        # Query the view and return the results as JSON
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM top_10_enrolled_courses')
            result = cursor.fetchall()
            
            # Convert the result to a list of dictionaries
            courses = []
            for row in result:
                course = {
                    'course_id': row[0],
                    'course_name': row[1],
                    'num_students': row[2]
                }
                courses.append(course)
            
            # Return the courses as JSON
            return jsonify(courses)
    
    finally:
        db.commit()


@app.route('/top_10_students_with_highest_averages', methods=['GET'])
def top_10_students_with_highest_averages():
    try:
        # Create the view
        with db.cursor() as cursor:
            cursor.execute('CREATE OR REPLACE VIEW top_10_students_with_highest_averages AS '
                           'SELECT s.student_id, s.first_name, s.last_name, AVG(g.grade) AS average_grade '
                           'FROM students s '
                           'JOIN grades g ON s.student_id = g.student_id '
                           'GROUP BY s.student_id '
                           'ORDER BY average_grade DESC '
                           'LIMIT 10')
        
        # Query the view and return the results as JSON
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM top_10_students_with_highest_averages')
            result = cursor.fetchall()
            
            # Convert the result to a list of dictionaries
            students = []
            for row in result:
                student = {
                    'student_id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'average_grade': row[3]
                }
                students.append(student)
            
            # Return the students as JSON
            return jsonify(students)
    
    finally:
        db.commit()

@app.route('/number_of_students', methods=['GET'])
def number_of_students():
    try:
        # Query the database for the number of students
        with db.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM students')
            result = cursor.fetchone()
            num_students = result[0]

        # Return the number of students as a JSON response
        return jsonify({'num_students': num_students})
    
    finally:
        db.close()
   
###
# The functions below should be applicable to all Flask apps.
###
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
