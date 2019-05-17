# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Participant(UserMixin, db.Model):
    """
    Create a Particapant table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'participants'

   
    email = db.Column(db.String(60), primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    firstname = db.Column(db.String(60), index=True)
    lastname = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def is_active(self):
      """True, as all users are active."""
      return True

    def get_id(self):
      """Return the email address to satisfy Flask-Login's requirements."""
      return self.email

    def is_authenticated(self):
      """Return True if the user is authenticated."""
      return self.authenticated

    def is_anonymous(self):
      """False, as anonymous users aren't supported."""
      return False 

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Participant: {}>'.format(self.email)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Participant.query.get((user_id))


class Workshop(db.Model):
    """
    Create a Workshop table
    """

    __tablename__ = 'workshops'

    id = db.Column(db.Integer, primary_key=True)
    workshop = db.Column(db.String(60), unique=True)
    date=db.Column(db.String(10))
    description = db.Column(db.String(200))
    room_no = db.relationship('Room', backref='worksop',
                                 lazy='dynamic')

    def __repr__(self):
        return '<Workshop: {}>'.format(self.workshop)



class Room(db.Model):
    """
    Create a Room table
    """

    __tablename__ = 'rooms'

    room_no=db.Column(db.String(3),primary_key=True)
    capacity=db.Column(db.Integer)
    workshop=db.Column(db.Integer,db.ForeignKey('workshops.id'))

    def __repr__(self):
        return '<room: {}>'.format(self.room_no)
