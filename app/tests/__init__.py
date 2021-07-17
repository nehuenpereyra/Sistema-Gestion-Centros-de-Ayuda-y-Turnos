import unittest
from app import create_app
from app.db import db
from app.models.user_permission import UserPermission
from app.models.user_role import UserRole


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        with self.app.app_context():
            print("[DatabaseInitializer]")
            db.drop_all()
            print(f" - database dropped")
            db.create_all()
            print(f" - database created")
            self.create_permissions()
            self.create_roles()

        
    
    def tearDown(self):
        print("Se borra la app")

    def create_permissions(self):
        with self.app.app_context():
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
        with self.app.app_context():
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
