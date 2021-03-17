from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///flask_feedback'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "nevertell"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toobar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)

        db.session.commit()
        session['username'] = new_user.username
        flash("Welcome! Successfully created your account")

        return redirect(f"/users/{new_user.username}")

    else:
        return render_template('/users/register.html', form=form)

@app.route('/users/<username>')
def show_user(username):
    """Show logged in users"""

    user = User.query.get(username)
    return render_template('users/show.html', user=user)


@app.route('/login', methods=["GET", "POST"])
def login_user():

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            return "login success"
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)
