from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)

from .models import User

class PostForm(FlaskForm):
    meal_type = RadioField('What type of meal did you have?', choices=['Breakfast', 'Lunch', 'Dinner', 'Other'])
    home_rest = RadioField('Did you make it or did you have it at a restaurant?', choices=['Homemade','Restaurant'])
    title = StringField("Title your post (what did you eat?)", [InputRequired(), Length(min=1, max=100)])
    text = TextAreaField("For homemade meals, describe the recipe and ingredients. For restaurant meals, discuss the restaurant environment, service, pricing, and location.", validators = [InputRequired(), Length(min=5, max=1000)])
    image = FileField('Post a picture of your meal (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only')])
    submit = SubmitField("Post!")

class CommentForm(FlaskForm):
    text = TextAreaField("Add a comment", validators=[InputRequired(), Length(min=5, max=500)])
    submit = SubmitField("Enter")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
            InputRequired(), 
            Length(min=12, max=40, message="Password must be between 12 and 40 characters."), 
            Regexp("^(?=.*[a-z])", message="Password must have a lowercase character."),
            Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character."),
            Regexp("^(?=.*\\d)", message="Password must contain a number."),
            Regexp("(?=.*[@$!%*#?&])", message="Password must contain a special character."),
        ])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Update your username if you'd like (Note: you will have to login again)", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update")
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")
