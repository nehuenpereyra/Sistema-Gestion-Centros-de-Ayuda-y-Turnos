
from app.db import db
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import random
from app.models.user_role import UserRole, link_user_role


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.relationship(
        "UserRole", secondary=link_user_role, back_populates="users")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    @hybrid_property
    def get_email(self):
        return self.email

    @hybrid_property
    def get_first_name(self):
        return self.first_name

    @hybrid_property
    def get_last_name(self):
        return self.last_name

    # @hybrid_property
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f'<User {self.email}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    def has_role(self, role):
        for each in self.roles:
            if each.name == role:
                return True
        return False
