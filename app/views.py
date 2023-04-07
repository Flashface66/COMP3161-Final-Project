"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from flask_login import login_user, logout_user, current_user, login_required, user_loaded_from_request

from app import app, login_manager
from flask import flash, jsonify, render_template, request, redirect, url_for
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
    print(current_user.id)

    return render_template('home.html', user=user)


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render website's login page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    
    # cursor.execute('SELECT * FROM notquiteourvle.students')
    form = LoginForm()

    if form.validate_on_submit():
        # Get the username and password values from the form.
        username = form.username.data
        password = form.password.data
        # user_type = form.user_type.data

        # if user_type == '1':
        #     db_table = 'students'
        #     user_class = Student
        #     id = 'student'
        # elif user_type == '2':
        #     db_table = 'lecturers'
        #     user_class = Lecturer
        #     id = 'lect'

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM notquiteourvle.users WHERE account_id=%s"
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        user_data = results[0] if results else None

        if user_data:
            user = User(user_data['account_id'])
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid user ID or user type.')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render website's registration page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    
    form = RegisterStudentForm()


    

    if form.validate_on_submit():
        # Get the form data submitted by the user
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user_type = form.user_type.data
        if user_type == '1':
            db_table = 'students'
            
            id = 'student'
        elif user_type == '2':
            db_table = 'lecturers'
            
            id = 'lect'

      
        cursor = db.cursor()
        query = "INSERT INTO notquiteourvle.{} (first_name, last_name, email, user_type) VALUES (%s, %s, %s, %s)".format(db_table)
        print(query)
        values = (first_name, last_name, email, user_type)
        cursor.execute(query, values)

     
        user_id = cursor.lastrowid
        user_query = "INSERT INTO notquiteourvle.users (account_id,first_name, last_name, email, user_type, account_type) VALUES (%s, %s, %s, %s, %s, %s)"
        print(user_query)
        values = ( user_id, first_name, last_name, email, user_type, db_table)
        cursor.execute(user_query, values)
        db.commit()

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


@app.route('/courses_display')
@login_required
def courses_display():
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
    # print(courses)
    return render_template('courses.html',  courses=courses)

@app.route('/courses')
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
    return jsonify(courses)
   

@app.route('/students')
@login_required
def students():
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.students "
    cursor.execute(student_query)
    students = cursor.fetchall()

    

    return jsonify(students)

@app.route('/students_display')
@login_required
def students_display():
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.students "
    cursor.execute(student_query)
    students = cursor.fetchall()

    
    # print(students)
    return render_template("students.html", students=students)


@app.route('/lecturers')
@login_required
def lecturers():
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    lecturer_query = "SELECT * FROM notquiteourvle.lecturers "
    cursor.execute(lecturer_query)
    lecturers = cursor.fetchall()

    

    return jsonify(lecturers)

@app.route('/lecturers_display')
@login_required
def lecturers_display():
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    lecturer_query = "SELECT * FROM notquiteourvle.lecturers "
    cursor.execute(lecturer_query)
    lecturers = cursor.fetchall()

    

    return render_template("lecturers.html", lecturers=lecturers)



@app.route('/<course_id>/lecturers')
@login_required
def lecturer_student(course_id):
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    

    # Retrieve the courses for the given student ID
    course_query = """
    
        SELECT lecturers.lect_id, lecturers.first_name, lecturers.last_name
        FROM notquiteourvle.lecturers
        JOIN lect_course ON lecturers.lect_id = lect_course.lect_id
        WHERE lect_course.course_id = %s;
     """
    cursor.execute(course_query, (course_id,))
    courses = cursor.fetchall()

    return jsonify(courses)



@app.route('/<user_id>/courses')
@login_required
def user_courses(user_id):
    """Render user's courses page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
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

    return jsonify(courses)


@app.route('/<user_id>/courses_display')
@login_required
def user_courses_display(user_id):
    """Render user's courses page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
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

    return render_template("user_course.html", courses=courses)    



@app.route('/<course_id>/students')
@login_required
def course_student(course_id):
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

  
    # Retrieve the courses for the given student ID
    course_query = """
        SELECT students.student_id, students.first_name, students.last_name
        FROM notquiteourvle.students
        JOIN student_course ON students.student_id = student_course.student_id
        WHERE student_course.course_id = %s;
     """
    cursor.execute(course_query, (course_id,))
    students = cursor.fetchall()

    
    return jsonify(students)

@app.route('/<course_id>/students_display')
@login_required
def course_student_display(course_id):
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.courses WHERE course_id = %s"
    cursor.execute(student_query, (course_id,))
    courses = cursor.fetchone()

    # Retrieve the courses for the given student ID
    course_query = """
        SELECT students.student_id, students.first_name, students.last_name
        FROM notquiteourvle.students
        JOIN student_course ON students.student_id = student_course.student_id
        WHERE student_course.course_id = %s;
     """
    cursor.execute(course_query, (course_id,))
    students = cursor.fetchall()

    
    return render_template('students.html', students=students, courses=courses)



    


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
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
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
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
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
        update_query = '''
                            UPDATE notquiteourvle.lect_course SET lect_id = %s WHERE course_id = %s;
                        '''
        cursor.execute(update_query, (lect_id, course_id))
    else:
        # If course ID does not exist, insert a new row
        insert_query = '''
                            INSERT INTO notquiteourvle.lect_course (lect_id, course_id) VALUES (%s, %s);
                        '''
        cursor.execute(insert_query, (lect_id, course_id))

    db.commit()
    return jsonify({"lect_id": lect_id, "course_id": course_id})



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
