from wtforms import (
    StringField,
    PasswordField,
    RadioField
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Regexp ,Optional
from wtforms import ValidationError,validators
from models import User


# Define registration form
class register_form(FlaskForm):
    # Define displayname field with optional, length and regex validators
    displayname = StringField(
        validators=[
            Optional(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z]*$",
                0,
                "Display Name must have only letters.",
            )
            ]
    )
    # Define username field with required, length and regex validators
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, periods or underscores.",
            ),
        ]
    )
    # Define password field with required and length validators
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    # Define confirm password field with required, length and equal to validators
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match!"),
        ]
    )
    # Define custom validator for username
    def validate_uname(self, username):
        # Check if username already exists in the database
        if User.query.filter_by(username=username.data).first():
            # Raise validation error if username already exists
            raise ValidationError("Username already taken!")
# Define login form        
class login_form(FlaskForm):
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[InputRequired(), Length(min=3, max=20) ]
    )
