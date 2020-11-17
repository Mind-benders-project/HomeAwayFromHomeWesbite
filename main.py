import os
import secrets 
from PIL import Image 
from flask import Flask, render_template, url_for, flash, redirect, request 
from datetime import datetime 
from sqlalchemy import text 
''' imports text from sqlalchemy that will convert a string to text which further can be used as as sql query '''
from flask_sqlalchemy import SQLAlchemy 
''' SQLAlchemy is used to implement database for this project'''
from flask_bcrypt import Bcrypt 
''' Bcrypt is used for storing the password in encrypted manner to database'''
from flask_login import LoginManager, UserMixin,login_user, current_user, logout_user, login_required 
''' these are various login related modules which helps in implementing trivial tasks related to login and signup'''

'''secrets is imported to assign a secrete key for security of cookies'''
'''pillow is imported for resizing image'''
''' imports various modules from flask'''
''' Used for getting current date and time'''
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
''' secrete_key will protect against modifying cookies and cross-site requests, forgery attacks'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
'''sets up a database with name 'db' '''
db = SQLAlchemy(app) 
'''binds 'db' for our flask application'''
bcrypt = Bcrypt(app) 
''' binds bcrypt encryption for our flask application'''
login_manager = LoginManager(app) 
'''login manager contains the code that lets your application and Flask-Login work together, such as how to load a user from an ID, where to send users when they need to log in, and the like'''
login_manager.login_view = 'login' 
''' flashes message 'login' if user is expected to be logged in .If the login view is not set, it will abort with a 401 error'''
login_manager.login_message_category = 'info' 
''' customize the login message category'''

''' It is used to reload the user object from the user ID stored in the session'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 
    '''returns an instance of class User with id 'user_id' '''

'''stores all the details of user ,inherits db.Model for our database structure and UserMixin for authentication purpose '''
class User(db.Model, UserMixin):
    ''' This class acts as a table (relation) in our database. following attributes acts as column in our table'''
    ''' 'id' is predefined name for id column in sqlalchemy ,it is autoincrement in nature by default , db.Column makes it a column in our database db for table 'User'. First argument passed gives the Datatype of the values that this coulmn will store, second argument 'primary key' is set true to make this attribute a primary key for this class(table)'''
    id = db.Column(db.Integer, primary_key=True) 
    user_name = db.Column(db.String(20), nullable=False) 
    ''' Here also first argument gives datatype for the coulmn and second argument gives nullability of the coulmn , nullble=false implies that none of the row in this column will have a null value'''
    email = db.Column(db.String(120), unique=True, nullable=False) 
    ''' unique= true implies that all the values in this particular column will be either unique or null but definitely non-duplicate values'''
    contact = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg') 
    ''' default argument gives the default value to be stored for a row in this column if input is not given explicitly'''
    password = db.Column(db.String(60), nullable=False) 
    ''' integer passed with String gives the maximum no. of characters that string may have'''
    user_rating = db.Column(db.Float, default=1, nullable=False) 
    '''Overall rating of the user '''
    user_coins = db.Column(db.Integer, default=0, nullable=False) 
    ''' coins earned by the user '''
    role = db.Column(db.Integer, default=1, nullable=False)
    dob = db.Column(db.String(60), nullable=False)
    count5 = db.Column(db.Integer, default=0, nullable=False)
    ''' stores how many people gave 5 rating to the specific user '''
    count4 = db.Column(db.Integer, default=0, nullable=False)
    ''' stores how many user gave 4 rating to the user '''
    count3 = db.Column(db.Integer, default=0, nullable=False)
    count2 = db.Column(db.Integer, default=0, nullable=False)
    count1 = db.Column(db.Integer, default=1, nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True) 
    '''this 'posts' is an object for relationship between two classes 'Post' and 'User' .There is a foreign key in class 'Post' which is refereing to a column of class 'User' '''
    
    '''specific columns in return will be shown when a instance of this class is printed'''
    def __repr__(self): 
        return f"User('{self.user_name}', '{self.email}', '{self.image_file}', '{self.role}')" 

'''This table stores all the data related to the posts done by User and inherits db.Model class'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    '''id is primary key for each post'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    '''stores id of user who posted it , refers 'id' column of User table'''
    user_name = db.Column(db.String(20), nullable=False) 
    ''' stores name of user who posted it '''
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pincode = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    furnishing_type = db.Column(db.Integer,default=0, nullable=False)
    refrigerator = db.Column(db.Boolean,default=0, nullable=False)
    washing_machine = db.Column(db.Boolean, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Boolean,default=0, nullable=False)
    almirah = db.Column(db.Boolean,default=0, nullable=False)
    bed = db.Column(db.Boolean,default=0, nullable=False)
    geyser = db.Column(db.Boolean,default=0, nullable=False)
    gas_stove = db.Column(db.Boolean,default=0, nullable=False)
    sofa = db.Column(db.Boolean,default=0, nullable=False)
    availability = db.Column(db.Integer,default=0, nullable=False)
    landloard_nature = db.Column(db.Text,nullable=True)
    neighbours_nature = db.Column(db.Text,nullable=True)
    comments = db.Column(db.Text, nullable=True)
    flat_rating =db.Column(db.Integer, default=1, nullable=False)
    nearby = db.Column(db.Text, nullable=True)
    picture1 = db.Column(db.String(20), nullable=False) 
    '''stores name with extension of image '''
    picture2 = db.Column(db.String(20), nullable=True)
    picture3 = db.Column(db.String(20), nullable=True)
    picture4 = db.Column(db.String(20), nullable=True)
    picture5 = db.Column(db.String(20), nullable=True)

    '''these columns in return will be printed when instance of this class is printed'''
    def __repr__(self):
        return f"Post('{self.user_id}', '{self.date_posted}', '{self.picture1}', '{self.bedrooms}', '{self.bed}', '{self.furnishing_type}')"
'''This table stores which user reviewed which user, It also overwrites the previous rating given by user with latest review the user has given'''
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    '''id is concatination of user_id(who gave rating) and user_id(to whom the rating is given) ensuring that only one rating of a user is considered for a specific user'''
    Rating = db.Column(db.Integer, nullable=False) 
    '''stores the latest rating given by the user'''
    
    '''specific columns in return will be shown when a instance of this class is printed'''
    def __repr__(self):
        return f"Review('{self.id}', '{self.Rating}')"
'''routes the application to this function when path is '/' or '/home' , renders the home page , takes an html page as an argument and list of posts'''
@app.route("/")
@app.route("/home")
def home():
    posts= Post.query.all()
    return render_template('home.html', posts=posts)

global searched 
'''stores the posts which satisfies the search request'''
searched = []

global nofilter 
'''used to check whther filter is applied or not , 0 for nofilter , 1 if filter applied'''
nofilter = 0
global area 
'''stores area which is searched '''
global city 
'''stores name of city which is searched '''
global state 
'''stores name of state which is searched'''

'''route the application here when the path is '/search' , performs search on area,city and state and redirects it to 'show_post' in case of invalid search , it renders the same page(search page) '''
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm() 
    ''' gets an object of form from search page along with values entered by user in the form '''
    ''' condition checked when search button is  '''
    if form.validate_on_submit(): 
        global searched
        global area
        global city
        global state
        area = form.area.data
        city = form.city.data
        state = form.state.data

        searched = Post.query.filter((Post.area==form.area.data) & (Post.city==form.city.data) & (Post.state==form.state.data)).all() 
        ''' returns posts which satisfy the searched condition '''
        ''' redirects to 'show_post' '''
        return redirect(url_for('show_post')) 
    return render_template('search.html', form=form)


'''redirected from 'search', this function renders each post(enumerate each post) based on search and filter conditions , sends filter form and list of posts which satisfy search condition'''
@app.route("/show_post", methods=['GET', 'POST'])
def show_post():
    form = Filter()
    global nofilter
    global searched
    global area
    global city
    global state

    if nofilter == 0:
        nofilter = 1
        '''if filter is not applied it is redirected to show posts without any flitering'''
        return redirect(url_for('show_post')) 
    else:
        if form.validate_on_submit():
            nofilter = 1
            minrent = form.minrent.data
            maxrent = form.maxrent.data
            flat_rating = form.flat_rating.data

            str1 = "(Post.area=="+"'"+area+"'"+") & (Post.city=="+"'"+city+"'"+") & (Post.state=="+"'"+state+"'"+") & "

            str1 = str1+ "(Post.rent >="+str(minrent)+") & (Post.rent <="+str(maxrent)+") & (Post.flat_rating >="+str(flat_rating)+") & "

            if form.furnishing_type.data and form.furnishing_type1.data and form.furnishing_type2.data:
                str1 = str1 + "((Post.furnishing_type=='2') or (Post.furnishing_type=='1') or (Post.furnishing_type=='0')) & "
            elif form.furnishing_type.data and form.furnishing_type1.data:
                str1 = str1 + "((Post.furnishing_type=='2') or (Post.furnishing_type=='1')) & "
            elif form.furnishing_type1.data and form.furnishing_type2.data:
                str1 = str1 + "((Post.furnishing_type=='1') or (Post.furnishing_type=='0')) & "
            elif form.furnishing_type.data and form.furnishing_type2.data:
                str1 = str1 + "((Post.furnishing_type=='2') or (Post.furnishing_type=='0')) & "
            elif form.furnishing_type.data:
                str1 = str1 + "(Post.furnishing_type=='2') & "
            elif form.furnishing_type1.data:
                str1 = str1 + "(Post.furnishing_type=='1') & "
            elif form.furnishing_type2.data:
                str1 = str1 + "(Post.furnishing_type=='0') & "

            if form.refrigerator.data:
                str1 = str1 + "(Post.refrigerator==True) &"
            if form.washing_machine.data:
                str1 = str1 + "(Post.washing_machine==True) &"
            if form.ac.data:
                str1 = str1 + "(Post.ac==True) &"
            if form.almirah.data:
                str1 = str1 + "(Post.almirah==True) &"
            if form.bed.data:
                str1 = str1 + "(Post.bed==True) &"
            if form.geyser.data:
                str1 = str1 + "(Post.geyser==True) &"
            if form.gas_stove.data:
                str1 = str1 + "(Post.gas_stove==True) &"
            if form.sofa.data:
                str1 = str1 + "(Post.sofa==True) &"

            br = ""
            if form.bedrooms.data:
                br = br + "(Post.bedrooms==0) or"
            if form.bedrooms2.data:
                br = br + "(Post.bedrooms==1) or"
            if form.bedrooms3.data:
                br = br + "(Post.bedrooms==2) or"
            if form.bedrooms4.data:
                br = br + "(Post.bedrooms==3) or"

            
            br = br[:-2]
            if br == '':
                br = "True"

            br = "("+br+")"
            str1 = str1 + br 
            ''' all the requirements are concatenated in str1 according to the filter form '''
            searched1 = Post.query.filter(text(str1)).all() 
            '''searched1 is a list of all the posts which satisfies searched and filter conditions , posts are filtered on the basis of filter conditions in str1'''
            '''renders show_post.html and passes filter form and filtered list of posts'''
            return render_template('show_post.html',form=Filter(), posts=searched1) 
            
    '''if filter is not applied all searched posts are rendered on show_post.html '''
    return render_template('show_post.html',form=form, posts=searched)


from forms import RegistrationForm, LoginForm, Post_info, UpdateProfile, SearchForm, Filter,OthersProfile 
'''imports some modules from 'form' '''
'''routes the application when path is '/reward' , renders the reward page '''
@app.route("/")
@app.route("/reward")
def reward():
    return render_template('reward.html')


'''routes the application here when the path is '/register' , performs authentication related to registration ,flashes message according to status of registration'''
@app.route("/register", methods=['GET', 'POST'])
def register():
    '''if the user has stored login password in cookies then he will be directly logged in and redirected to home page'''
    if current_user.is_authenticated: 
        return redirect(url_for('home'))

    form = RegistrationForm() 
    '''gives details feed in registration form '''
    ''' checks for validation when 'register' button is clicked '''
    if form.validate_on_submit(): 
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        '''encrypts entered password '''
        user = User(user_name=form.name.data, email=form.email.data,contact=form.contact.data,dob=form.dob.data,role=form.role.data,password=encrypted_password) 
        '''creates an object of 'User' class that can be used to insert a tuple in the 'User' table '''
        db.session.add(user) 
        ''' adds a tuple in table '''
        db.session.commit() 
        ''' commits the changes performed in database'''
        flash('Your account has been created, please LOGIN ', 'success') 
        '''flash message when registered successfully'''
        ''' redirects to login page '''
        return redirect(url_for('login')) 

    ''' in case of invalid registration user is redirected back to registration page'''
    return render_template('register.html', form=form) 

''' This function is used to implement login functionality ,routes application here when path is '/login' '''
@app.route("/login", methods=['GET', 'POST'])
def login():
    '''checks for authentication of the user , whether credentials are already stored or not '''
    if current_user.is_authenticated:
        ''' if authenticated , redirects to 'home' page ''' 
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        '''checks for password of the user , compares it with encrypted password and return true or false '''
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=True) 
            '''on successfully authentication , user is logged in and his/her credentials are stored '''
            next_page = request.args.get('next') 
            '''as of now we do not have a next page '''
            ''' user is redirected to 'home' page '''
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            ''' on un-successfull login , message is flashed in red '''
            flash('Login Unsuccessful. Incorrect email or password', 'danger') 
    return render_template('login.html', form=form)


'''routes application here when path is '/logout' , logouts a user from the application and redirects him/her to home page '''
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user() 
    '''inbuilt function from flask_login which handles the functionalities related to logout and redirects the user to home page '''
    return redirect(url_for('home'))

''' routes the application here when path is '/profile', checks for current user and shows him/her his/her profile page  '''
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    '''queries all the posts from database '''
    posts= Post.query.all() 
    ''' form for updating profile , which updates profile picture of user'''
    form = UpdateProfile() 
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) 
            '''saves the picture given by user'''
            current_user.image_file = picture_file 
            ''' sets the user profile as the inputed image'''
        db.session.commit() 
        ''' commits the changes done in database '''
        flash('Your account has been updated!', 'success') 
        ''' flashes message on successfully updating profile picture '''
        return redirect(url_for('profile'))
   
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    ''' sets the profile picture as updated(if updated) image''' 
    return render_template('profile.html', image_file=image_file, form=form, posts=posts) 

#     image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
#     return render_template('profile.html', image_file=image_file)

'''routes application here when path is '/others_profile' , this function is used to render profile page of other users '''
@app.route("/others_profile", methods=['GET', 'POST'])
@login_required
def others_profile():
    posts= Post.query.all()
    form = OthersProfile()
    user_id=request.args.get('user_id') 
    ''' id of the user whose profile is being viewed '''
    user = User.query.get(user_id) 
    ''' instance of the user whose profile is being viewed '''
    a=0
    ''' it stores the rating given by user in a variable 'a' when 'Rate' button is clicked '''
    if form.validate_on_submit(): 
        if form.rating.data== '4':
            a=5
        elif form.rating.data == '3':
            a=4
        elif form.rating.data == '2':
            a=3
        elif form.rating.data== '1':
            a=2
        elif form.rating.data== '0':
            a=1


        idd = (current_user.id*100000) + int(user_id) 
        '''six digit combined composite id for user who rated and whom it rated '''
        ''' if the user is rating for a particular user for the first time '''
        if (Review.query.filter(Review.id==idd).count() == 0 ): 
            if(a==5):
                user.count5=user.count5+1
            elif(a==4):
                user.count4=user.count4+1
            elif(a==3):
                user.count3=user.count3+1
            elif(a==2):
                user.count2=user.count2+1
            elif(a==1):
                user.count1=user.count1+1
            review = Review(id=idd , Rating=a )
            db.session.add(review)
            db.session.commit()
        else:
            rev = Review.query.get(idd)
            prev_rating= rev.Rating
            ''' gets the previous rating done by the user for that user '''
            if(prev_rating==5):
                user.count5=user.count5-1
            elif(prev_rating==4):
                user.count4=user.count4-1
            elif(prev_rating==3):
                user.count3=user.count3-1
            elif(prev_rating==2):
                user.count2=user.count2-1
            elif(prev_rating==1):
                user.count1=user.count1-1
            db.session.commit()
            rev.Rating=a
            '''assigning new rating to the corresponding user pair '''
            if(a==5):
                user.count5=user.count5+1
            elif(a==4):
                user.count4=user.count4+1
            elif(a==3):
                user.count3=user.count3+1
            elif(a==2):
                user.count2=user.count2+1
            elif(a==1):
                user.count1=user.count1+1
            a=0
            db.session.commit()

        db.session.commit()
        user.user_rating = round(((user.count5*5 + user.count4*4 + user.count3*3 + user.count2*2 + user.count1*1 -1)/(user.count5 + user.count4 + user.count3 + user.count2 + user.count1 -1)),2)
        ''' updates overall user rating after each new rating '''
        db.session.commit()
        user.user_coins = round((user.user_rating * (user.count5 + user.count4 + user.count3 + user.count2 + user.count1) * Post.query.filter_by(user_id=user_id).count())/10,2) 
        ''' updates coin of the user according to no. of ratings he got , no. of posts he has done and what rating he got '''
        db.session.commit()
        flash('You succesfully rated this account!', 'success') 
        '''flashes message if the rating was done successfully '''
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        return render_template('others_profile.html', image_file=image_file,user=user, form=form, posts=posts)
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    '''fetches the profile image of the user whose profile is viewed '''
    return render_template('others_profile.html', image_file=image_file,user=user, form=form, posts=posts)

''' saves the profile picture in the allocated folder with random name and returns the name of image along with extension of image '''
def save_picture(form_picture):
    if not form_picture:
        image = url_for('static', filename='profile_pics/' + "default.jpeg")
        return image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i = i.resize((150, 150))
    i.save(picture_path)

    return picture_fn 
''' saves the picture of the posts in the designated folder , returns name of image with extension '''
def save_post_picture(form_picture):
    if not form_picture:
        image = url_for('static', filename='posted_pics/' + "default.png")
        return image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/posted_pics', picture_fn)

    i = Image.open(form_picture)
    i = i.resize((1100, 800))
    i.save(picture_path)

    image_file = url_for('static', filename='posted_pics/' + picture_fn)

    return image_file
''' routes the application here if the path is '/post' , creates a object of 'Post' and adds a tuple in the Post when a new post is created , fetches the data for post from the form Post_info '''
'''login_required function can not be executed if current user is not logged in'''
@app.route("/post", methods=['GET', 'POST'])
@login_required 
def post():
    form = Post_info() 
    '''fetches information entered in form for posting'''
    if form.validate_on_submit():
       post = Post(author = current_user,user_name=current_user.user_name , state= form.state.data , city = form.city.data , area = form.area.data, date_posted= datetime.now(), pincode=form.pincode.data, rent =form.rent.data, furnishing_type = form.furnishing_type.data , refrigerator = form.refrigerator.data , washing_machine = form.washing_machine.data , 
                ac=form.ac.data , almirah=form.almirah.data, bed=form.bed.data, geyser=form.geyser.data, gas_stove=form.gas_stove.data, sofa=form.sofa.data, availability=1, landloard_nature=form.landloard_nature.data, 
                neighbours_nature=form.neighbours_nature.data, comments=form.comments.data, flat_rating=form.flat_rating.data, nearby=form.nearby.data, picture1=save_post_picture(form.picture1.data), 
                picture2=save_post_picture(form.picture2.data), picture3=save_post_picture(form.picture3.data), picture4=save_post_picture(form.picture4.data), picture5=save_post_picture(form.picture5.data), bedrooms=form.bedrooms.data)
       db.session.add(post) 
       '''adds a new tuple(object) post in table Post'''
       db.session.commit()
       flash('Your post posted successfully!', 'success')
       '''flashes message when post is created sucessfully '''
       '''redirects to home page after successfully creating the post '''
       return redirect(url_for('home')) 
    '''renders template post.html if post is not posted/created'''    
    return render_template('post.html', form=form) 




if __name__ == '__main__':
    app.run(debug=True)

