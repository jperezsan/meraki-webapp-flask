from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User, Role


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    user_role = SelectField('Role', choices=None)

    def __init__(self, roles):
        super(RegistrationForm, self).__init__()
        role_list = []
        for r in roles:
            role_list += [r.name]

        self.user_role.choices = role_list

    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangeRoleForm(FlaskForm):
    user_role = SelectField('Role', choices=None)
    user_id = HiddenField('user_id')
    submit = SubmitField('Change Role')

    def __init__(self, roles):
        super(ChangeRoleForm, self).__init__()
        role_list = []
        for r in roles:
            role_list += [r.name]

        self.user_role.choices = role_list
