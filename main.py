import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin,login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    user_rating = db.Column(db.Float, default=1, nullable=False)
    user_coins = db.Column(db.Integer, default=0, nullable=False)
    role = db.Column(db.Integer, default=1, nullable=False)
    dob = db.Column(db.String(60), nullable=False)
    count5 = db.Column(db.Integer, default=0, nullable=False)
    count4 = db.Column(db.Integer, default=0, nullable=False)
    count3 = db.Column(db.Integer, default=0, nullable=False)
    count2 = db.Column(db.Integer, default=0, nullable=False)
    count1 = db.Column(db.Integer, default=1, nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_name}', '{self.email}', '{self.image_file}', '{self.role}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
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
    picture1 = db.Column(db.String(20), nullable=False, default='default.jpeg')
    picture2 = db.Column(db.String(20), nullable=True)
    picture3 = db.Column(db.String(20), nullable=True)
    picture4 = db.Column(db.String(20), nullable=True)
    picture5 = db.Column(db.String(20), nullable=True)


    def __repr__(self):
        return f"Post('{self.user_id}', '{self.date_posted}', '{self.picture1}', '{self.bedrooms}', '{self.bed}', '{self.furnishing_type}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Review('{self.id}', '{self.Rating}')"

@app.route("/")
@app.route("/home")
def home():
    posts= Post.query.all()
    return render_template('home.html', posts=posts)

global searched
searched = []

global nofilter
nofilter = 0
global area
global city
global state
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        global searched
        global area
        global city
        global state
        area = form.area.data
        city = form.city.data
        state = form.state.data

        searched = Post.query.filter((Post.area==form.area.data) & (Post.city==form.city.data) & (Post.state==form.state.data)).all()
        return redirect(url_for('show_post'))
    return render_template('search.html', form=form)



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
            searched1 = Post.query.filter(text(str1)).all()
            return render_template('show_post.html',form=Filter(), posts=searched1)

    return render_template('show_post.html',form=form, posts=searched)


from forms import RegistrationForm, LoginForm, Post_info, UpdateProfile, SearchForm, Filter,OthersProfile
@app.route("/")
@app.route("/reward")
def reward():
    return render_template('reward.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_name=form.name.data, email=form.email.data,contact=form.contact.data,dob=form.dob.data,role=form.role.data,password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, please LOGIN ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Incorrect email or password', 'danger')
    return render_template('login.html', form=form)



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    posts= Post.query.all()
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
   
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', image_file=image_file, form=form, posts=posts)




    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('profile.html', image_file=image_file)

@app.route("/others_profile", methods=['GET', 'POST'])
@login_required
def others_profile():
    posts= Post.query.all()
    form = OthersProfile()
    user_id=request.args.get('user_id')
    user = User.query.get(user_id)
    a=0
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
            flash(user.count5)
            flash(user.count4)
            flash(idd)
            flash(rev.Rating)



        db.session.commit()
        user.user_rating = round(((user.count5*5 + user.count4*4 + user.count3*3 + user.count2*2 + user.count1*1 -1 )/(user.count5 + user.count4 + user.count3 + user.count2 + user.count1)),2)
        db.session.commit()
        user.user_coins = round((user.user_rating * (user.count5 + user.count4 + user.count3 + user.count2 + user.count1) * Post.query.filter_by(user_id=user_id).count())/10,2)
        db.session.commit()
        flash('You succesfully rated this account!', 'success')
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        return render_template('others_profile.html', image_file=image_file,user=user, form=form, posts=posts)
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('others_profile.html', image_file=image_file,user=user, form=form, posts=posts)


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
    i.save(picture_path)

    return picture_fn

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

@app.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    form = Post_info()
    if form.validate_on_submit():
       post = Post(author = current_user,user_name=current_user.user_name , state= form.state.data , city = form.city.data , area = form.area.data, date_posted= datetime.now(), pincode=form.pincode.data, rent =form.rent.data, furnishing_type = form.furnishing_type.data , refrigerator = form.refrigerator.data , washing_machine = form.washing_machine.data , 
                ac=form.ac.data , almirah=form.almirah.data, bed=form.bed.data, geyser=form.geyser.data, gas_stove=form.gas_stove.data, sofa=form.sofa.data, availability=1, landloard_nature=form.landloard_nature.data, 
                neighbours_nature=form.neighbours_nature.data, comments=form.comments.data, flat_rating=form.flat_rating.data, nearby=form.nearby.data, picture1=save_post_picture(form.picture1.data), 
                picture2=save_post_picture(form.picture2.data), picture3=save_post_picture(form.picture3.data), picture4=save_post_picture(form.picture4.data), picture5=save_post_picture(form.picture5.data), bedrooms=form.bedrooms.data)
       db.session.add(post)
       db.session.commit()
       flash('Your post posted successfully!', 'success')
       return redirect(url_for('home'))
        
    return render_template('post.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)

