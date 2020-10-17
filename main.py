from flask import Flask, render_template, url_for, flash, redirect
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
        return f"User('{self.user_name}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pincode = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    no_of_rooms = db.Column(db.Integer, nullable=False)
    furnished = db.Column(db.Integer,default=0, nullable=False)
    refridgerator = db.Column(db.Integer,default=0, nullable=False)
    washing_machine = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Integer,default=0, nullable=False)
    almirah = db.Column(db.Integer,default=0, nullable=False)
    bed = db.Column(db.Integer,default=0, nullable=False)
    geyser = db.Column(db.Integer,default=0, nullable=False)
    sofaset = db.Column(db.Integer,default=0, nullable=False)
    availability = db.Column(db.Integer,default=0, nullable=False)
    nature_of_landlord = db.Column(db.Text,nullable=True)
    comments = db.Column(db.Text, nullable=True)
    flat_rating =db.Column(db.Integer, default=1, nullable=False)
    near_by = db.Column(db.Text, nullable=True)
    image1 = db.Column(db.String(20), nullable=False, default='default.jpeg')
    image2 = db.Column(db.String(20), nullable=True)
    image3 = db.Column(db.String(20), nullable=True)
    image4 = db.Column(db.String(20), nullable=True)
    image5 = db.Column(db.String(20), nullable=True)





    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/search")
def search():
    return render_template('search.html')

from forms import RegistrationForm, LoginForm
@app.route("/register", methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=True)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Incorrect email or password', 'danger')
    return render_template('login.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

