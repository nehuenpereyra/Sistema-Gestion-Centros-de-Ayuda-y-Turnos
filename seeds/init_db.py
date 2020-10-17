from werkzeug.security import generate_password_hash

from flask_seeder import Seeder

from app.models.user import User
from app.models.user_permission import UserPermission
from app.models.user_role import UserRole
from app.models.configuration import Configuration


class InitialSeeder(Seeder):

    # Inicializa las tablas del sistema
    def run(self):
        if User.find_by_email("admin@admin.com") == None:
            rol = UserRole(name="Administrador", permissions=[
                           UserPermission(name="configuration_update"),
                           UserPermission(name="user_index"),
                           UserPermission(name="user_create"),
                           UserPermission(name="user_update"),
                           UserPermission(name="user_delete")])
            UserRole(name="Operador").save()
            User(name="admin", surname="admin", email="admin@admin.com",
                 username="admin_root", password=generate_password_hash("123123"), roles=[rol]).save()
            print("Se cargo correctamente el primer usuario administrador")

        if Configuration.query.filter(Configuration.query.exists()).scalar() == None:
            Configuration().save()
            print("Se cargo correctamente la configuración inicial de la página")
