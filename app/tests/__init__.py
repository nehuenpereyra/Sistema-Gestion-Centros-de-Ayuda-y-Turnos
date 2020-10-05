import os
import unittest
from app import create_app, delete_app
from app.resources.user import User
from werkzeug.security import generate_password_hash

class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        #self.client = self.app.test_client()

        with self.app.app_context():
            BaseTestClass.create_user("admin@admin.com","admin","admin","admin","123123")

    def tearDown(self):
        with self.app.app_context():
            delete_app(self.app)
        

    @staticmethod
    def create_user(email, username, first_name, last_name, password):
        User(username= username ,email=email, 
        first_name=first_name, last_name=last_name,
        password=generate_password_hash(password)).save()