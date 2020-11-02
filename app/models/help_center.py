
import os
import shutil

from flask import current_app

from app.db import db

from app.models.help_center_type import HelpCenterType
from app.models.town import Town
from app.models.turn import Turn


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
    turns = db.relationship("Turn", back_populates="help_center")
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
            os.makedirs(self.get_upload_path())
        else:
            db.session.commit()

    def remove(self):
        if self.id:
            shutil.rmtree(self.get_upload_path())

            self.turns.do(lambda each: each.remove())
            db.session.delete(self)
            db.session.commit()

    @ property
    def town(self):
        if not self.town_object:
            self.town_object = Town.get(self.town_id)
        return self.town_object

    @ town.setter
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

    def get_upload_path(self):
        return f'{current_app.config["UPLOAD_FOLDER"]}/help_centers/{self.id}'

    def get_view_protocol_path(self):
        return os.path.join(self.get_upload_path(), f"{self.name} - Protocolo.pdf")

    def update_view_protocol(self):

        if self.has_view_protocol:
            self.view_protocol_file.save(self.get_view_protocol_path())
            self.view_protocol_file = None
        else:
            os.remove(self.get_view_protocol_path())

        self.view_protocol_updated = False

    view_protocol = property(
        fget=None, fset=set_view_protocol, fdel=remove_view_protocol, doc=None)

    def reserve_turn(self, email_donante, telefono_donante, hora_inicio, fecha):
        if not Turn.all_reserved_date(self.id, fecha).any_satisfy(lambda each: each.day_hour.time() == hora_inicio):
            Turn(help_center=self,
                 email=email_donante,
                 donor_phone_number=telefono_donante,
                 day_hour=fecha).save()

    @staticmethod
    def delete(id):
        center = HelpCenter.query.get(id)
        if center:
            center.remove()
            return center
        return None

    def has_turn(self, turn):
        return self.turns.includes(turn)
