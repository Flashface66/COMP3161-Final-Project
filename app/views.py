"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from flask_login import login_user, logout_user, current_user, login_required

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
    query = "SELECT * FROM notquiteourvle.students WHERE student_id = %s"

    cursor.execute(query, (current_user.id,))

    student = cursor.fetchone()
    print(student)

    return render_template('home.html', student=student)

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

        # Query database for a user based on the username and password submitted.
        cursor = db.cursor(dictionary=True)
        query = f"SELECT * FROM notquiteourvle.students WHERE student_id=%s"
        print("help")
        print(query)
        cursor.execute(query, (username,))
        
 
        results = cursor.fetchall()
        # print(results)
        user = results[0] if results else None  

        # Check if user exists and password matches
        if user:
            # Log in the user
            login_user(User(user['student_id']))
            # Remember to flash a message to the user
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username or Password is incorrect.', 'danger')

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

      
        cursor = db.cursor()
        query = "INSERT INTO students (first_name, last_name, email) VALUES (%s, %s, %s)"
        values = (first_name, last_name, email)
        cursor.execute(query, values)

        db.commit()
        student_id = cursor.lastrowid
        
        flash(f'You have successfully registered with student ID: {student_id}.', 'success')
        user = User(student_id)
        login_user(user)
        return redirect(url_for('home'))
        

    return render_template('register.html', form=form)


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
def load_user(id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM notquiteourvle.students WHERE student_id=%s"
    cursor.execute(query, (id,))
    results = cursor.fetchall()
    # print(results)
    user = results[0] if results else None    
    if user:
        return User(user['student_id'])



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
   

@app.route('/<student_id>/courses_display')
@login_required
def student_course_display(student_id):
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.students WHERE student_id = %s"
    cursor.execute(student_query, (student_id,))
    student = cursor.fetchone()

    # Retrieve the courses for the given student ID
    course_query = """
        SELECT courses.*, student_course.*
        FROM courses
        JOIN student_course ON courses.course_id = student_course.course_id
        WHERE student_course.student_id = %s
    """
    cursor.execute(course_query, (student_id,))
    courses = cursor.fetchall()

    return render_template('student_course.html', student=student, courses=courses)


@app.route('/<student_id>/courses')
@login_required
def student_course(student_id):
    """Render student's my course page."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Passwordnt",
        database="notquiteourvle"
    )
    cursor = db.cursor(dictionary=True)

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.students WHERE student_id = %s"
    cursor.execute(student_query, (student_id,))
    student = cursor.fetchone()

    # Retrieve the courses for the given student ID
    course_query = """
        SELECT courses.*, student_course.*
        FROM courses
        JOIN student_course ON courses.course_id = student_course.course_id
        WHERE student_course.student_id = %s
    """
    cursor.execute(course_query, (student_id,))
    courses = cursor.fetchall()

    return jsonify(courses)

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
    student = cursor.fetchone()

    # Retrieve the courses for the given student ID
    course_query = """
    
        SELECT students.student_id, students.first_name, students.last_name
        FROM notquiteourvle.students
        JOIN student_course ON students.student_id = student_course.student_id
        WHERE student_course.course_id = %s;
     """
    cursor.execute(course_query, (course_id,))
    courses = cursor.fetchall()

    
    return render_template('student_course.html', student=student, courses=courses)


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

    # Retrieve the student's information
    student_query = "SELECT * FROM notquiteourvle.courses WHERE course_id = %s"
    cursor.execute(student_query, (course_id,))
    student = cursor.fetchone()

    # Retrieve the courses for the given student ID
    course_query = """
    
        SELECT students.student_id, students.first_name, students.last_name
        FROM notquiteourvle.students
        JOIN student_course ON students.student_id = student_course.student_id
        WHERE student_course.course_id = %s;
     """
    cursor.execute(course_query, (course_id,))
    courses = cursor.fetchall()

    return jsonify(courses)
    

@app.context_processor
def inject_student():
    """Pass the student object to all templates."""
    if current_user.is_authenticated:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Passwordnt",
            database="notquiteourvle"
        )
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM notquiteourvle.students WHERE student_id = %s"

        cursor.execute(query, (current_user.id,))  
        student = cursor.fetchone()
        # print(student)
        return dict(student=student)
    else:
        return dict(student={})
  

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")




###
# The functions below should be applicable to all Flask apps.
###

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
