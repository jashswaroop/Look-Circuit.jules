from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Full Name')
    age = StringField('Age')
    gender = StringField('Gender')
    height = StringField('Height (e.g., 5\'11" or 180cm)')
    body_shape = StringField('Body Shape (e.g., Pear, Apple)')
    location_climate = StringField('Location / Climate')
    fashion_style = StringField('Fashion Style (e.g., Gen-Z, Millennial)')
    submit = SubmitField('Update')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please choose a different one.')

class StyleGuideForm(FlaskForm):
    fashion_preferences = StringField('Fashion Preferences')
    budget = StringField('Budget')
    lifestyle = StringField('Lifestyle')
    social_activities = StringField('Social Activities')
    fashion_risk_tolerance = StringField('Fashion Risk Tolerance')
    comfort_vs_style = StringField('Comfort vs. Style Priority')
    preferred_colors = StringField('Preferred Colors')
    avoided_colors = StringField('Colors to Avoid')
    brand_preferences = StringField('Brand Preferences')
    preferred_stores = StringField('Preferred E-commerce Stores')
    submit = SubmitField('Save Style Guide')
