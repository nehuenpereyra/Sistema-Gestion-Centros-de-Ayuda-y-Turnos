from datetime import datetime, date, time, timedelta
from sqlalchemy import Date, cast, and_

from app.db import db


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
    def update(id, id_center, email, donor_phone_number, day_hour):
        turn = Turn.query.get(id)
        if turn:
            turn.id_center = id_center
            turn.email = email
            turn.donor_phone_number = donor_phone_number
            user.day_hour = day_hour
            turn.save()
            return turn
        return None
