
import os

from flask import current_app

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
    has_view_protocol = db.Column(
        db.Boolean, nullable=False, unique=False, default=False)
    view_protocol_file = None
    view_protocol_updated = False
    latitude = db.Column(db.Float, nullable=True, unique=False)
    longitude = db.Column(db.Float, nullable=True, unique=False)

    def save(self):
        if self.view_protocol_updated:
            self.update_view_protocol()
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

    def set_view_protocol(self, file):
        self.has_view_protocol = True
        self.view_protocol_file = file
        self.view_protocol_updated = True

    def remove_view_protocol(self):
        self.has_view_protocol = False
        self.view_protocol_file = None
        self.view_protocol_updated = True

    def get_view_protocol_full_path(self):
        return f'{current_app.config["UPLOAD_FOLDER"]}/help_centers/{self.id}/{self.name} - Protocolo.pdf'

    def update_view_protocol(self):

        if self.has_view_protocol:
            view_protocol_path = os.path.dirname(
                self.get_view_protocol_full_path())

            if not os.path.exists(view_protocol_path):
                os.makedirs(view_protocol_path)

            self.view_protocol_file.save(self.get_view_protocol_full_path())
            self.view_protocol_file = None
        else:
            os.remove(self.get_view_protocol_full_path())

        self.view_protocol_updated = False

    view_protocol = property(
        fget=None, fset=set_view_protocol, fdel=remove_view_protocol, doc=None)
