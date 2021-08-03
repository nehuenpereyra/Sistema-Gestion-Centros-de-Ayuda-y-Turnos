import unittest

from app import create_app
from app.db import db


class BaseTestClass(unittest.TestCase):
    def setUp(self):  
        self.app = create_app()
        if self.app.config['DB_NAME'] != "grupo20_test":
            self.fail("Configure la base de dato de test con el nombre 'grupo20_test'.")
        with self.app.app_context():
            self.init_db()
        

    def init_db(self):
        db.drop_all()
        print(f" - database dropped")
        db.create_all()
        print(f" - database created")