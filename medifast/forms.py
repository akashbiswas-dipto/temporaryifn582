from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField,BooleanField,SelectField
from wtforms.validators import InputRequired, DataRequired, email, EqualTo, Length, AnyOf

class SignUpForm(FlaskForm):
    """Form for user sign up."""
    username = StringField("Username:", validators = [InputRequired(), Length(max=12, message="Length is within 12 characters only")])
    password = PasswordField("Password:", validators = [InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(max=8, message="Password length should not exceed 8")])
    confirm = PasswordField("Confirm Password:", validators=[InputRequired()])
    firstname = StringField("First Name:", validators = [InputRequired()])
    surname = StringField("Surname:", validators = [InputRequired()])
    email = StringField("Email:", validators = [InputRequired(), email()])
    phone = StringField("Phone Number:", validators = [InputRequired()])
    tc = BooleanField("Agree with Privacy Policy", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LogInForm(FlaskForm):
    """Form for user log in"""
    email = StringField("Email:", validators= [InputRequired(), email()])
    password = StringField("Password:", validators=[InputRequired()])
    submit = SubmitField("Log In")

class OrderForm(FlaskForm):
    """Form for user to order"""
    address = StringField("Address:", validators=[InputRequired()])
    customer_name = StringField("Name:", validators= [InputRequired()])
    customer_email = StringField("Email:", validators = [InputRequired(), email()])
    customer_phone = StringField("Phone:", validators = [InputRequired()])
    delivery_type = SelectField("Delivery Type:", choices=[(1, 'Express (15-20mins)'), (2, 'Regular (30-45mins)'), (3, 'Green Delivery'), (4, 'Pick Up')], validators=[DataRequired()])
    payment_type = SelectField("Payment Method:", choices=[(1, 'Credit Card'), (2, 'Bank Debit'), (3, 'Cash on Delivery')], validators=[DataRequired()])
    submit = SubmitField("Place Order")
