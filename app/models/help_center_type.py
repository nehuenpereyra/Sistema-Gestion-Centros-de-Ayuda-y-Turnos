
from app.db import db


class HelpCenterType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    help_centers = db.relationship("HelpCenter", back_populates="center_type")

    @staticmethod
    def all():
        return HelpCenterType.query.all()

    @staticmethod
    def get(id):
        return HelpCenterType.query.get(id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
