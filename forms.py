from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo , Regexp
from __main__ import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    contact = StringField('Contact',validators=[DataRequired(),Length(min=10, max=10),Regexp('^[0-9]+$') ])
    dob = DateField('Date of Birth [DD/MM/YYYY]', format='%d/%m/%Y', validators=[DataRequired()])
    role = RadioField('Role', choices=[(1,'Tenant'),(0,'Landlord')] , validators=[DataRequired()])
    submit = SubmitField('Register')



    def validate_contact(self, contact):
        user = User.query.filter_by(contact=contact.data).first()
        if user:
            raise ValidationError('Account with that contact no. already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account with that email already exists')


