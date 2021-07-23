import unittest
from app import create_app


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        
    
    def tearDown(self):
        print("Se borra la app")

    