from . import BaseTestClass

class UserTestCase(BaseTestClass):
    
    def test_create_user(self):
        with self.app.app_context():
            self.assertEqual("admin@admin.com",User.find_by_email("admin@admin.com").get_email)
        print("[Correct] Test Create user")