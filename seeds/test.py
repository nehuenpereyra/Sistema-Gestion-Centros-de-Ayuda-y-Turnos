from flask_seeder import Seeder
from app.models.user import User
from werkzeug.security import generate_password_hash

class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    if User.find_by_email("admin@admin.com") == None:
        User(username= "admin",email="admin@admin.com", 
        first_name="admin", last_name="admin",
        password=generate_password_hash("123123")).save()
        print("Usuario admin creado")

