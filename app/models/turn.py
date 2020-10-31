from datetime import datetime, date, time, timedelta

from app.db import db


class Turn(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    day_hour = db.Column(db.DateTime, nullable=False, unique=False)
    donor_phone_number = db.Column(db.String(16), nullable=False, unique=True)
    help_center = db.relationship(
        "HelpCenter", back_populates="turns")
    help_center_id = db.Column(
        db.Integer, db.ForeignKey('help_center.id'), nullable=False)

    @staticmethod
    def all_reserved():
        return Turn.query.all()

    @staticmethod
    def all_reserved_date(date):
        return Turn.query.filter(Turn.day_hour.date == date)

    @staticmethod
    def all_free_date(date):

        turns = []
        turn_date = datetime(date.year, date.month, date.day, 9, 0, 0, 0)
        for x in range(14):
            if turn_date >= date.today():
                turns.append({"date": turn_date})
                turn_date = turn_date + timedelta(minutes=30)

        #turn.match(Turn.all_reserved(), lambda each1, each2: each1.time != each2.time)
        return turns

    @staticmethod
    def reservation(center_id, email_donante, telefono_donante, hora_inicio, fecha):
        # if Turn.all_reserved_date(fecha).detect(lambda each: each.help_center_id != center_id and each.day_hour.time != hora_inicio):
        #   Turn(help_center=HelpCenter.query.get(center_id),
        #       email=email_donante,
        #       donor_phone_number=telefono_donante,
        #       day_hour=datetime(fecha.year, fecha.month, fecha.day, hora_inicio[0:1], hora_inicio[2:3]))
        pass
