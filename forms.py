from flask_wtf import FlaskForm 
''' imports flaskform to create forms '''
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, ValidationError, IntegerField, TextAreaField 
''' imports various fields which are used to create forms '''
from wtforms.fields.html5 import IntegerRangeField 
''' imported to implement sliding bar in rent filter option '''
from flask_wtf.file import FileField, FileAllowed 
''' imported to handle files read and validation '''
from wtforms.validators import DataRequired, Length, Email, EqualTo , Regexp 
''' imports various validators which are used in validating various fields of forms '''
from __main__ import User 
'''imports user class from main '''

''' This class creates a form for login purpose , inherits from class FlaskForm '''
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()]) 
    ''' accepts email of user who is trying to login '''
    password = PasswordField('Password', validators=[DataRequired()]) 
    ''' accepts password of user who is trying to login '''
    submit = SubmitField('Login') 
    '''button to initialize login '''
    
''' This class creates a form for Registering new users, inherits from class FlaskForm '''
class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)]) 
    ''' accepts the name of user as string field '''
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    ''' accepts email of user '''
    password = PasswordField('Password', validators=[DataRequired()])
    ''' accepts password of user '''
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    ''' matches the password with password in above field''' 
    contact = StringField('Contact',validators=[DataRequired(),Length(min=10, max=10),Regexp('^[0-9]+$') ]) 
    '''accepts the contact no. of user and checks whether the contact is of valid type or not '''
    dob = DateField('Date of Birth [DD/MM/YYYY]', format='%d/%m/%Y', validators=[DataRequired()]) 
    ''' accepts valid date of birth from user '''
    role = RadioField('Role', choices=[(1,'Tenant'),(0,'Landlord')] , validators=[DataRequired()]) 
    ''' accepts role of user via radio button'''
    submit = SubmitField('Register') 
    ''' Register button to initiate the registration process '''


    '''This funtion validates that whether a user with given contact already exists or not '''
    def validate_contact(self, contact):
        user = User.query.filter_by(contact=contact.data).first()
        if user:
            raise ValidationError('Account with that contact no. already exists')
            ''' raises an exception if existing contact no. is used for registration '''
    '''Checks whether a user with given email id already exists or not '''
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account with that email already exists') 
            '''raises an exception if existing email is used to register '''
            
'''This below class is a 'form' for the search purpose , it inherits class FlaskForm and gives a structute to accepts strings to perform search '''
class SearchForm(FlaskForm):
    state = StringField('State', validators=[DataRequired(), Length(max=30)])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    area = StringField('Colony', validators=[DataRequired()])
    submit = SubmitField('Search')
    
''' Below class is also a 'form' for the filter purpose , it inherits class FlaskForm and provides appropriate structure for the form which is used to get data for filtering '''
class Filter(FlaskForm):
    '''various fields on the basis of which filtering can be done '''
    minrent = IntegerRangeField('Minimum rent')
    maxrent = IntegerRangeField('Maximum rent')
    furnishing_type = BooleanField('Fully-Furnished')
    furnishing_type1 = BooleanField('Semi-Furnished')
    furnishing_type2 = BooleanField('Not furnished')
    bedrooms4 = BooleanField('4-BHK')
    bedrooms3= BooleanField('3-BHK')
    bedrooms2 = BooleanField('2-BHK')
    bedrooms = BooleanField('1-BHK')
    refrigerator = BooleanField('Refrigerator')
    washing_machine = BooleanField('Washing Machine')
    ac = BooleanField('AC')
    almirah = BooleanField('Almirah')
    bed = BooleanField('Bed')
    geyser = BooleanField('Geyser')
    gas_stove = BooleanField('Gas Stove')
    sofa = BooleanField('Sofa Set')
    flat_rating=IntegerRangeField('Minimum Rating')
    submit = SubmitField('Apply')
    ''' button to apply the given filter '''
    
'''Below class is a 'form', it inherits class FlaskForm and provides a structure for form which accepts all the details regarding a post'''
class Post_info(FlaskForm):
    state = StringField('State', validators=[DataRequired()]) 
    city = StringField('City', validators=[DataRequired()])
    area = StringField('Area', validators=[DataRequired()])
    pincode = IntegerField('Pincode', validators=[DataRequired()])
    rent = IntegerField('Rent', validators=[DataRequired()])
    furnishing_type = RadioField('Furnishing Type', choices=[(2,'Fully-Furnished'),(1,'Semi-Furnished'),(0,'Not furnished')] , validators=[DataRequired()])
    refrigerator = BooleanField('Refrigerator') 
    ''' checkbox to get whether this amenity is provided or not '''
    washing_machine = BooleanField('Washing Machine')
    ac = BooleanField('AC')
    almirah = BooleanField('Almirah')
    bed = BooleanField('Bed')
    geyser = BooleanField('Geyser')
    gas_stove = BooleanField('Gas Stove')
    sofa = BooleanField('Sofa Set')
    landloard_nature = TextAreaField('Nature of Landlord',validators=[DataRequired(), Length(min=2, max=200)]) 
    ''' nature of landlord according to the user , takes text as input '''
    neighbours_nature = TextAreaField('Nature of Neighbours',validators=[Length(min=2, max=200)]) 
    ''' nature of neighbours according to the user , takes text as input '''
    comments = TextAreaField('Comments',validators=[Length(min=2, max=200)]) 
    ''' additional comment regarding the place, takes text as input '''
    nearby = TextAreaField('Nearby',validators=[DataRequired(), Length(min=2, max=200)]) 
    ''' nearby areas , takes text as input '''
    flat_rating=IntegerField('Rate 1-10', validators=[DataRequired()]) 
    ''' overall rating of the place from the point of user who is posting '''
    picture1 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])]) 
    '''Filefield which takes file as input of the given formats '''
    picture2 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture3 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture4 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    picture5 = FileField("Property's Pic", validators=[FileAllowed(['jpg','png','jpeg'])])
    bedrooms = RadioField('No. of bedrooms', choices=[(3,'4-BHK'),(2,'3-BHK'),(1,'2-BHK'),(0,'1-BHK')] , validators=[DataRequired()])
    submit = SubmitField('Submit')

'''Below class is a form with one button and 1 file field to update profile picture of the user , it inherits class FlaskForm'''
class UpdateProfile(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])]) 
    ''' file field which accepts files of mentioned format '''
    submit = SubmitField('Update') 
    '''update button '''
    
'''Below class is used to create a form for Rating a user, it has 1 radio-field and 1 button to Rate the user , it inherits class FlaskForm '''
class OthersProfile(FlaskForm):
    rating = RadioField('Rating', choices=[(4,'5 stars'),(3,'4 stars'),(2,'3 stars'),(1,'2 stars'),(0,'1 star')]) 
    '''rating provided by user '''
    submit = SubmitField('Rate') 
    ''' Rate button '''