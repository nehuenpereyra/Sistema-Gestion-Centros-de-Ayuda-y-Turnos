from datetime import datetime, date, time, timedelta

from app.db import db
from app.models.help_center import HelpCenter
from sqlalchemy import Date, cast, and_


class Turn(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    day_hour = db.Column(db.DateTime, nullable=False, unique=False)
    donor_phone_number = db.Column(db.String(16), nullable=False)
    help_center = db.relationship(
        "HelpCenter", back_populates="turns")
    help_center_id = db.Column(
        db.Integer, db.ForeignKey('help_center.id'), nullable=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def remove(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()

    @staticmethod
    def all_reserved(center_id):
        return Turn.query.filter(Turn.help_center_id == center_id).all()

    @staticmethod
    def all_reserved_date(center_id, in_date):
        return Turn.query.filter(and_(cast(Turn.day_hour, Date) == in_date), (Turn.help_center_id == center_id)).all()

    @staticmethod
    def all_free_time(center_id, in_date):

        turns = []
        turn_date = datetime(in_date.year, in_date.month,
                             in_date.day, 9, 0, 0, 0)
        for x in range(14):
            # if turn_date > date.today():
            turns.append(turn_date)
            turn_date = turn_date + timedelta(minutes=30)

        return turns.match_all(Turn.all_reserved_date(center_id, in_date), lambda each1,
                               each2: each1 != each2.day_hour)

    @staticmethod
    def reservation(center_id, email_donante, telefono_donante, hora_inicio, fecha):
        if not Turn.all_reserved_date(center_id, fecha).any_satisfy(lambda each: each.day_hour.time() == hora_inicio):
            Turn(help_center=HelpCenter.query.get(center_id),
                 email=email_donante,
                 donor_phone_number=telefono_donante,
                 day_hour=fecha).save()
        pass
