
from app.db import db

from app.models.help_center_type import HelpCenterType
from app.models.town import Town


class HelpCenter(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=False)
    address = db.Column(db.String(32), nullable=False, unique=False)
    phone_number = db.Column(db.String(16), nullable=False, unique=True)
    opening_time = db.Column(db.Time, nullable=False, unique=False)
    closing_time = db.Column(db.Time, nullable=False, unique=False)
    center_type = db.relationship(
        "HelpCenterType", back_populates="help_centers")
    center_type_id = db.Column(
        db.Integer, db.ForeignKey('help_center_type.id'), nullable=False)
    town_id = db.Column(db.Integer, nullable=False, unique=False)
    town_object = None
    web_url = db.Column(db.String(64), nullable=True, unique=True)
    email = db.Column(db.String(32), nullable=True, unique=True)
    published = db.Column(db.Boolean, nullable=True,
                          unique=False, default=True)
    request_status = db.Column(db.Boolean, nullable=True, unique=False)

    view_protocol = db.Column(
        db.Boolean, nullable=False, unique=False, default=False)

    latitude = db.Column(db.Float, nullable=True, unique=False)
    longitude = db.Column(db.Float, nullable=True, unique=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @property
    def town(self):
        if not self.town_object:
            self.town_object = Town.get(self.town_id)
        return self.town_object

    @town.setter
    def town(self, value):
        self.town_id = value.id
        self.town_object = value
