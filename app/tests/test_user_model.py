from . import BaseTestClass 
from werkzeug.security import generate_password_hash

from app.resources.user import User
from app.models.user_role import UserRole

class UserModelTest(BaseTestClass):
    """User model test suite"""

    def test_user_new(self):
        with self.app.app_context():
            roles = {each.name: each for each in UserRole.query.all()}
            admin_user = User(name="Test", surname="Lopez", email="admin@admin.com",
                          username="Juanchuz", password=generate_password_hash("admin123"),
                          roles=[roles["Administrador"]])
            admin_user.save()
            result = User.find_by_email("admin@admin.com").get_email
        self.assertEqual("admin@admin.com", result)