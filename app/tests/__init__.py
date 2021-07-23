import unittest
from app import create_app
from app.db import db


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        with self.app.app_context():
            self.init_db()
        

    def init_db(self):
        db.drop_all()
        print(f" - database dropped")
        db.create_all()
        print(f" - database created")