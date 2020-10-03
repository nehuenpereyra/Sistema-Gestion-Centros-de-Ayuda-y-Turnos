from app.db import db
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)


    @hybrid_property
    def get_email(self):
        return self.email
    
    @hybrid_property
    def get_first_name(self):
        return self.first_name
    
    @hybrid_property
    def get_last_name(self):
        return self.last_name

    @staticmethod
    def all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def find_by_email_and_pass(email, password):
        return User.query.filter_by(email=email).filter_by(password=password).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f'<User {self.email}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()