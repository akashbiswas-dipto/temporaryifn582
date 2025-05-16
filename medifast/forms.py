from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, email

# reference
# class LoginForm(FlaskForm):
#     """Form for user login."""
#     email = StringField("email", validators = [InputRequired()])
#     password = PasswordField("Password", validators = [InputRequired()])
#     submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    """Form for user sign up."""
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    firstname = StringField("First Name", validators = [InputRequired()])
    surname = StringField("Surname", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired(), email()])
    phone = StringField("Phone Number", validators = [InputRequired()])
    submit = SubmitField("Make Account")