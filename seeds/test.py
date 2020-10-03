from flask_seeder import Seeder
from app.models.user import User

class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    if User.find_by_email("test2@test") == None:
        User(email="test2@test", first_name="test2",
    last_name="facilito2",password="test123123",username="test2").save()
        print("Usuario test1 creado")

