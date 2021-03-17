from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/ hashed password and return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn byte-string into normal (unicode utf8 string)
        hashed_utf8 = hashed.decode("utf8")
        new_user = cls(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        # return instance of user w/username and hashed pwd
        return new_user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return false."""

        u = User.query.filter_by(username=username).first()

        # u.password = crazy long string in database, pwd = what user typed into form
        if u and bcrypt.check_password_hash(u.passord, pwd):
            # return user instance (aka <User 3>)
            return u
        else:
            return False