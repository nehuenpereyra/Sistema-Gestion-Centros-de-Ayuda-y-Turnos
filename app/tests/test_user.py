from . import BaseTestClass 
from werkzeug.security import generate_password_hash

from app.db import db
from app.resources.user import User
from app.models.user_role import UserRole
from app.models.user_permission import UserPermission

class UserTest(BaseTestClass):
    """User model test suite"""

    def test_save(self):
        
        with self.app.app_context():

            # Inicializacion de la base de datos y datos necesarios
            self.init_db()
            self.create_permissions()
            self.create_roles()

            roles = {each.name: each for each in UserRole.query.all()}
            admin_user = User(name="admin", surname="admin", email="admin@admin.com",
                          username="admin", password=generate_password_hash("admin123"),
                          roles=[roles["Administrador"]])
            admin_user.save()
            result = User.find_by_email("admin@admin.com").get_email
        self.assertEqual("admin@admin.com", result)

    def test_update(self):

        with self.app.app_context():

            # Inicializacion de la base de datos y datos necesarios
            self.init_db()
            self.create_permissions()
            self.create_roles()

            roles = {each.name: each for each in UserRole.query.all()}
            admin_user = User(name="admin", surname="admin", email="admin@admin.com",
                          username="admin", password=generate_password_hash("admin123"),
                          roles=[roles["Administrador"]])
            mod_user = admin_user.update(admin_user.get_id, "admin2", "admin2", "admin2@admin.com", "admin2", roles["Administrador"], True, None)
        self.assertEqual(True, self.equal_user(admin_user, mod_user))
    
    def equal_user(self, user_one, user_two):
        if user_one.name==user_two.name and user_one.surname==user_two.surname and user_one.email==user_two.email and user_one.username==user_two.username: 
            return True
        return False

    def test_remove(self):
        pass



    def init_db(self):
        print("[DatabaseInitializer]")
        db.drop_all()
        print(f" - database dropped")
        db.create_all()
        print(f" - database created")

    def create_permissions(self):
        UserPermission(name="user_index").save()
        UserPermission(name="user_create").save()
        UserPermission(name="user_update").save()
        UserPermission(name="user_delete").save()
        print(f" - User Permissions OK")
        UserPermission(name="help_center_index").save()
        UserPermission(name="help_center_show").save()
        UserPermission(name="help_center_create").save()
        UserPermission(name="help_center_update").save()
        UserPermission(name="help_center_delete").save()
        UserPermission(name="help_center_certify").save()
        print(f" - Help Center Permissions OK")
        UserPermission(name="turn_index").save()
        UserPermission(name="turn_create").save()
        UserPermission(name="turn_update").save()
        UserPermission(name="turn_delete").save()
        print(f" - Turn Permissions OK")
    
    def create_roles(self):
        permissions = {each.name: each for each in UserPermission.query.all()}
            
        operator_permissions = [
        permissions["help_center_index"],
        permissions["help_center_show"],
        permissions["help_center_create"],
        permissions["help_center_update"],
        permissions["help_center_certify"],
        permissions["turn_index"],
        permissions["turn_create"],
        permissions["turn_update"],
        ]

        admin_role = UserRole(name="Administrador", permissions=list(permissions.values()))
        admin_role.save()
        print(f" - {admin_role.name} Role OK")

        operator_role = UserRole(name="Operador", permissions=operator_permissions)
        operator_role.save()
        print(f" - {operator_role.name} Role OK")
