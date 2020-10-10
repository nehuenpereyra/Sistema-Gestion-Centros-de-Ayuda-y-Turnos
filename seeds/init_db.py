from flask_seeder import Seeder
from app.models.user import User
from app.models.configuration import Configuration
from werkzeug.security import generate_password_hash

class InitialSeeder(Seeder):

  # Inicializa las tablas del sistema
  def run(self):
    
    if User.find_by_email("admin@admin.com") == None:
        User(username= "admin",email="admin@admin.com", 
        first_name="admin", last_name="admin",
        password=generate_password_hash("123123")).save()
        print("Se cargo correctamente el primer usuario administrador")

    if Configuration.query.filter(Configuration.query.exists()).scalar() == None:
        Configuration().save()
        print("Se cargo correctamente la configuración inicial de la página")
