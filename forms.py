from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, ValidationError, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo , Regexp
# from __main__ import User


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



class Post_info(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    area = StringField('Area', validators=[DataRequired()])
    pincode = IntegerField('Pincode', validators=[DataRequired()])
    rent = IntegerField('Rent', validators=[DataRequired()])
    furnishing_type = RadioField('Furnishing Type', choices=[(2,'Fully-Furnished'),(1,'Semi-Furnished'),(0,'Not furnished')] , validators=[DataRequired()])
    refrigerator = BooleanField('Refrigerator')
    washing_machine = BooleanField('Washing Machine')
    ac = BooleanField('AC')
    almirah = BooleanField('Almirah')
    bed = BooleanField('Bed')
    geyser = BooleanField('Geyser')
    gas_stove = BooleanField('Gas Stove')
    sofa = BooleanField('Sofa Set')
    landloard_nature = TextAreaField('Nature of Landlord',validators=[DataRequired(), Length(min=2, max=200)])
    neighbours_nature = TextAreaField('Nature of Neighbours',validators=[Length(min=2, max=200)])
    comments = TextAreaField('Comments',validators=[Length(min=2, max=200)])
    nearby = TextAreaField('Nearby',validators=[DataRequired(), Length(min=2, max=200)])
    flat_rating=IntegerField('Rate 1-10', validators=[DataRequired()])
    picture1 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture2 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture3 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture4 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture5 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    bedrooms = RadioField('No. of bedrooms', choices=[(3,'4-BHK'),(2,'3-BHK'),(1,'2-BHK'),(0,'1-BHK')] , validators=[DataRequired()])
    submit = SubmitField('Submit')