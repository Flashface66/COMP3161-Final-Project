from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SelectField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    

class RegisterStudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    user_type = SelectField('User Type', choices=[('1', 'Student'), ('2', 'Lecturer')], validators=[InputRequired()])
    

class SubmissionForm(FlaskForm):
    assignment =  FileField('Assignment', validators=[InputRequired()])
    
