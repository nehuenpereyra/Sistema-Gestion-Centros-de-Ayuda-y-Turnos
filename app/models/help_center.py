
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

    def __init__(self, name, address, phone_number, opening_time, closing_time, center_type, town, web_url=None, email=None, published=True, request_status=None, view_protocol=None, latitude=None, longitude=None):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.center_type = center_type
        self.town = town
        self.web_url = web_url
        self.email = email
        self.published = published
        self.request_status = request_status
        self.view_protocol = view_protocol
        self.latitude = latitude
        self.longitude = longitude
        self.turns = []

    def public_dict(self):
        return {
            "nombre": self.name,
            "direccion": self.address,
            "telefono": self.phone_number,
            "hora_apertura": self.opening_time.strftime("%H:%M"),
            "hora_cierre": self.closing_time.strftime("%H:%M"),
            "tipo": self.center_type.name,
            "web": self.web_url,
            "email": self.email
        }

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()
            os.makedirs(self.get_upload_path())
        else:
            db.session.commit()

        if self.view_protocol_updated:
            self.update_view_protocol()

    # def update(self,
    #     name=self.name,
    #     address=self.address,
    #     phone_number=self.phone_number,
    #     opening_time=self.opening_time,
    #     closing_time=self.closing_time,
    #     center_type=self.center_type,
    #     town=self.town,
    #     web_url=self.web_url,
    #     email=self.email,
    #     published=self.published,
    #     request_status=self.request_status,
    #     view_protocol=self.view_protocol,
    #     latitude=self.latitude,
    #     longitude=self.longitude)

    def remove(self):
        if self.id:
            shutil.rmtree(self.get_upload_path())

            self.turns.do(lambda each: each.remove())
            db.session.delete(self)
            db.session.commit()

    def is_in_pending_state(self):
        return self.request_status == None

    def is_in_rejected_state(self):
        return self.request_status == False

    def is_in_accepted_state(self):
        return self.request_status

    def accept_request(self):
        self.request_status = True

    def reject_request(self):
        self.request_status = False

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
        self.view_protocol_updated = bool(file) or (
            self.has_view_protocol and not bool(file))
        self.has_view_protocol = bool(file)
        self.view_protocol_file = file

    def get_upload_path(self):
        return f'{current_app.config["UPLOAD_FOLDER"]}/help_centers/{self.id}'

    def get_view_protocol_filename(self):
        return "Protocolo.pdf"

    def get_view_protocol_path(self):
        return os.path.join(self.get_upload_path(), self.get_view_protocol_filename())

    def update_view_protocol(self):

        if self.has_view_protocol:
            self.view_protocol_file.save(self.get_view_protocol_path())
            self.view_protocol_file = None
        else:
            os.remove(self.get_view_protocol_path())

        self.view_protocol_updated = False

    view_protocol = property(
        fget=None, fset=set_view_protocol, fdel=None, doc=None)

    def reserve_turn(self, email_donante, telefono_donante, hora_inicio, fecha):
        if not Turn.all_reserved_date(self.id, fecha).any_satisfy(lambda each: each.day_hour.time() == hora_inicio):
            Turn(help_center=self,
                 email=email_donante,
                 donor_phone_number=telefono_donante,
                 day_hour=fecha).save()

    @staticmethod
    def get(id):
        return HelpCenter.query.get(id)

    @staticmethod
    def get_public_center(id):
        return HelpCenter.query.filter_by(request_status=True, published=True, id=id).first()

    @staticmethod
    def all_published(page=1, per_page=None):
        query = HelpCenter.query.filter_by(request_status=True, published=True)
        return query.paginate(page=page, per_page=per_page, error_out=False).items, query.count()

    @staticmethod
    def delete(id):
        center = HelpCenter.query.get(id)
        if center:
            center.remove()
            return center
        return None

    def has_turn(self, turn):
        return self.turns.includes(turn)

    @staticmethod
    def search(search_query, help_center_state, page, per_page):
        query = HelpCenter.query

        if search_query:
            query = query.filter(HelpCenter.name.like(f"%{search_query}%"))

        if help_center_state:
            if help_center_state != "pending":
                query = query.filter_by(
                    request_status=help_center_state == "accepted")
            else:
                query = query.filter_by(request_status=None)

        return query.paginate(page=page, per_page=per_page, error_out=False)
