from . import BaseTestClass 
from werkzeug.security import generate_password_hash

from app.db import db
from app.resources.user import User
from app.models.user_role import UserRole
from app.models.user_permission import UserPermission

class UserTest(BaseTestClass):
    """User model test suite"""

    def setUp(self):
        super().setUp()

        self.create_permissions()
        self.create_roles()

        self.roles = {each.name: each for each in self.roles_list}
        self.admin_user = User(name="admin", surname="admin", email="admin@admin.com",
                          username="admin", password=generate_password_hash("admin123"),
                          roles=[self.roles["Administrador"]])
        self.operador_user = User(name="operador", surname="operador", email="operador@operador.com",
                          username="operador", password=generate_password_hash("operador123"),
                          roles=[self.roles["Operador"]])

    def test_get_by_id(self):
        with self.app.app_context():
            self.assertIsNone(User.get_by_id(2000))
            self.admin_user.save()
            self.assertEqual(User.get_by_id(self.admin_user.id), self.admin_user)

    def test_save(self):
        with self.app.app_context():
            self.assertEqual(User.find_by_email(self.admin_user.email), None)
            self.admin_user.save()
            self.assertEqual(User.find_by_email(self.admin_user.email), self.admin_user)

    def test_update(self):
        with self.app.app_context():      
            user2 = {
                "name" : "user2",
                "surname" : "user2",
                "email": "user2@operador.com",
                "username" : "operador",
                "password" : "operador123",
                "roles" : [self.roles["Operador"]],
                "is_active" : False
            }
            self.admin_user.save()
            user = self.admin_user.update(self.admin_user.id, user2["name"], user2["surname"], user2["email"], user2["username"], user2["roles"], user2["is_active"],  user2["password"])            
            user2["password"] = user.password
            self.assertEqual(True, self.userEqual(user, user2))

    def test_remove(self):
        with self.app.app_context():
            self.admin_user.save()
            self.assertEqual(User.find_by_email(self.admin_user.email), self.admin_user)
            self.admin_user.remove()
            self.assertEqual(User.find_by_email(self.admin_user.email), None)

    def test_has_role(self):
         with self.app.app_context():
            self.assertTrue(self.admin_user.has_role(self.admin_role.name))
            self.assertFalse(self.admin_user.has_role(self.operator_role.name))

            self.assertTrue(self.operador_user.has_role(self.operator_role.name))
            self.assertFalse(self.operador_user.has_role(self.admin_role.name))

    def create_permissions(self):
        self.permission_list = []
       
        self.permission_list.append(UserPermission(name="user_index"))
        self.permission_list.append(UserPermission(name="user_create"))
        self.permission_list.append(UserPermission(name="user_update"))
        self.permission_list.append(UserPermission(name="user_delete"))

        self.permission_list.append(UserPermission(name="help_center_index"))
        self.permission_list.append(UserPermission(name="help_center_show"))
        self.permission_list.append(UserPermission(name="help_center_create"))
        self.permission_list.append(UserPermission(name="help_center_update"))
        self.permission_list.append(UserPermission(name="help_center_delete"))
        self.permission_list.append(UserPermission(name="help_center_certify"))

        self.permission_list.append(UserPermission(name="turn_index"))
        self.permission_list.append(UserPermission(name="turn_create"))
        self.permission_list.append(UserPermission(name="turn_update"))
        self.permission_list.append(UserPermission(name="turn_delete"))
    
    def create_roles(self):
        self.roles_list = []
        
        permissions = {each.name: each for each in self.permission_list}
            
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

        self.admin_role = UserRole(name="Administrador", permissions=list(permissions.values()))
        self.roles_list.append(self.admin_role)
        self.operator_role = UserRole(name="Operador", permissions=operator_permissions)
        self.roles_list.append(self.operator_role)
    
    def userEqual(self, user1_obj, user2_dic):
        if  user1_obj.name==user2_dic["name"] and \
            user1_obj.surname==user2_dic["surname"] and \
            user1_obj.email==user2_dic["email"] and \
            user1_obj.username==user2_dic["username"] and \
            user1_obj.password==user2_dic["password"] and \
            user1_obj.roles[0].name==user2_dic["roles"][0].name and \
            user1_obj.is_active==user2_dic["is_active"]:
                return True
        return False

    
