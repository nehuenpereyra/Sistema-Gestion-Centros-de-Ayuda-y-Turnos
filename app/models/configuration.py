from sqlalchemy import event

from app.db import db


class Configuration(db.Model):

    __tablename__ = 'configuration'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, default="")
    description = db.Column(db.String(90), nullable=False, default="")
    contact_email = db.Column(
        db.String(30), unique=True, nullable=False, default="")
    pagination_elements = db.Column(db.Integer, nullable=False, default=10)
    enabled_site = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<Configuration {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
