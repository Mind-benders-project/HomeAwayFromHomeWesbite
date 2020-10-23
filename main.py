import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
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
    user_rating = db.Column(db.Integer, default=1, nullable=False)
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


@app.route("/")
@app.route("/home")
def home():
    posts= Post.query.all()
    return render_template('timeline.html' , posts=posts)


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/")
@app.route("/reward")
def reward():
    return render_template('reward.html')


from forms import RegistrationForm, LoginForm, Post_info, UpdateProfile

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
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
   
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', image_file=image_file, form=form)




    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('profile.html', image_file=image_file)


def save_picture(form_picture):
    if not form_picture:
        return "static/default.jpeg"
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/post", methods=['GET', 'POST'])
@login_required
def post():
    form = Post_info()
    if form.validate_on_submit():
       post = Post(author = current_user , state= form.state.data , city = form.city.data , area = form.area.data, date_posted= datetime.now(), pincode=form.pincode.data, rent =form.rent.data, furnishing_type = form.furnishing_type.data , refrigerator = form.refrigerator.data , washing_machine = form.washing_machine.data , 
                ac=form.ac.data , almirah=form.almirah.data, bed=form.bed.data, geyser=form.geyser.data, gas_stove=form.gas_stove.data, sofa=form.sofa.data, availability=1, landloard_nature=form.landloard_nature.data, 
                neighbours_nature=form.neighbours_nature.data, comments=form.comments.data, flat_rating=form.flat_rating.data, nearby=form.nearby.data, picture1=save_picture(form.picture1.data), 
                picture2=save_picture(form.picture2.data), picture3=save_picture(form.picture3.data), picture4=save_picture(form.picture4.data), picture5=save_picture(form.picture5.data), bedrooms=form.bedrooms.data)
       db.session.add(post)
       db.session.commit()
       flash('Your post posted successfully!', 'success')
       return redirect(url_for('home'))
        
    return render_template('post.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)

