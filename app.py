from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__) # this is the app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # 3 slashes is relative path, 4 slashes is absolute path
app.config['SECRET_KEY'] = 'thisisasecretkey' # this is a secret key for the app
bcrypt = Bcrypt(app) # this is the password hashing
db = SQLAlchemy(app) # this is the database

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('That username is taken. Please choose a different one.')

class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Add a function to create all tables within the Flask application context
def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Account created for {form.username.data}!</h1>'
    return render_template('register.html', form=form)

if __name__=="__main__":
    create_tables()
    app.run(debug=True)

