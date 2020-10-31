
from datetime import time

from flask_seeder import Seeder

from app.models.help_center import HelpCenter, HelpCenterType


class HelpCenterSeeder(Seeder):

    def run(self):

        print("[HelpCenterSeeder]")

        food_center_type = HelpCenterType(name="Centro de Alimentos")
        food_center_type.save()
        print(f" - {food_center_type.name} OK")

        clothing_center_type = HelpCenterType(name="Centro de Ropa")
        clothing_center_type.save()
        print(f" - {clothing_center_type.name} OK")

        blood_center_type = HelpCenterType(name="Centro de Sangre")
        blood_center_type.save()
        print(f" - {blood_center_type.name} OK")

        food_center_1 = HelpCenter(
            name="Centro el Arroz",
            address="Av 64 e40 y 41 nro 30",
            phone_number="+54 294 412-3456",
            opening_time=time(9),
            closing_time=time(16),
            center_type=food_center_type,
            town_id=25,
            web_url="https://arroz.centro.org",
            email="arroz@centro.org")
        food_center_1.save()
        print(f" - {food_center_1.name} OK")

        food_center_2 = HelpCenter(
            name="Centro la Papa",
            address="Av 80 e20 y 21 nro 90",
            phone_number="+54 294 410-2030",
            opening_time=time(9),
            closing_time=time(16),
            center_type=food_center_type,
            town_id=1,
            web_url="https://papa.centro.org",
            email="papa@centro.org",
            request_status=True)
        food_center_2.save()
        print(f" - {food_center_2.name} OK")

        clothing_center = HelpCenter(
            name="Centro la Camisa",
            address="Av 20 e42 y 43 nro 64",
            phone_number="+54 294 420-2040",
            opening_time=time(9),
            closing_time=time(16),
            center_type=clothing_center_type,
            town_id=25,
            web_url="https://camisa.centro.org",
            email="camisa@centro.org",
            request_status=False)
        clothing_center.save()
        print(f" - {clothing_center.name} OK")

        blood_center = HelpCenter(
            name="Centro la Gota",
            address="Av 46 e80 y 81 nro 70",
            phone_number="+54 294 440-2010",
            opening_time=time(9),
            closing_time=time(16),
            center_type=blood_center_type,
            town_id=20,
            web_url="https://gota.centro.org",
            published=False,
            request_status=True)
        blood_center.save()
        print(f" - {blood_center.name} OK")