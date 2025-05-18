from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, email, EqualTo, Length

class SignUpForm(FlaskForm):
    """Form for user sign up."""
    username = StringField("Username:", validators = [InputRequired(), Length(max=12, message="Length is within 12 characters only")])
    password = PasswordField("Password:", validators = [InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(max=8, message="Password length should not exceed 8")])
    confirm = PasswordField("Confirm Password:", validators=[InputRequired()])
    firstname = StringField("First Name:", validators = [InputRequired()])
    surname = StringField("Surname:", validators = [InputRequired()])
    email = StringField("Email:", validators = [InputRequired(), email()])
    phone = StringField("Phone Number:", validators = [InputRequired()])
    submit = SubmitField("Sign Up")

class LogInForm(FlaskForm):
    """Form for user log in"""
    email = StringField("Email:", validators= [InputRequired(), email()])
    password = StringField("Password:", validators=[InputRequired()])
    submit = SubmitField("Log In")