from . import BaseTestClass 
from werkzeug.security import generate_password_hash
from datetime import datetime, time, timedelta

from app.models.turn import Turn
from app.models.help_center import HelpCenter
from app.models.help_center_type import HelpCenterType
from app.models.town import Town
from app.models.town_phase import TownPhase


class TurnTest(BaseTestClass):
    """Turn model test suite"""

    def setUp(self):
        super().setUp()

        self.create_center_type()
        self.town_phase_1 = TownPhase(id=0, title="")
        self.town_1 = Town(id=0,name="",phase=self.town_phase_1)
        self.create_help_centers()

        self.day_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day+1, 13, 0)
        self.turn_one = Turn(
                email="juan@gmail.com",
                day_hour=self.day_datetime,
                donor_phone_number="2214053283",
                help_center=self.food_center_1
            )
        
    def test_all_reserved(self):
        with self.app.app_context():
            self.assertEqual(Turn.all_reserved(self.food_center_1.id), [])
            self.turn_one.save()
            self.assertEqual(Turn.all_reserved(self.food_center_1.id), [self.turn_one])
            turn_two = Turn(
                email="juan@gmail.com",
                day_hour=self.day_datetime + timedelta(minutes=30),
                donor_phone_number="2214053283",
                help_center=self.food_center_1
            )
            turn_two.save()
            self.assertEqual(Turn.all_reserved(self.food_center_1.id), [self.turn_one, turn_two]) 

    def test_remove(self):
        with self.app.app_context():
            self.turn_one.save()
            self.assertEqual(Turn.all_reserved(self.food_center_1.id), [self.turn_one])
            self.turn_one.remove()
            self.assertEqual(Turn.all_reserved(self.food_center_1.id), [])
        
    
    def test_is_pending(self):
        with self.app.app_context():
            self.turn_one.save()
            self.assertEqual(self.turn_one.is_pending(), True)
            turn_two = Turn(
                email="juan@gmail.com",
                day_hour=datetime(datetime.today().year, datetime.today().month, datetime.today().day-1,13,0),
                donor_phone_number="2214053283",
                help_center=self.food_center_1
            )
            turn_two.save()
            self.assertEqual(turn_two.is_pending(), False)

    def test_all_free_time(self):
        with self.app.app_context():
            turns_free_time = Turn.all_free_time(self.food_center_1.id, self.day_datetime.date())
            take_datetime = turns_free_time[0]
            turn_two = Turn(
                email="juan@gmail.com",
                day_hour=take_datetime,
                donor_phone_number="2214053283",
                help_center=self.food_center_1
            )
            turn_two.save()
            new_turns_free_time = Turn.all_free_time(self.food_center_1.id, self.day_datetime.date())
            self.assertEqual(new_turns_free_time.detect(lambda each: each == take_datetime), None)
            


    def test_all_reserved_date(self):
        with self.app.app_context():
            self.assertEqual(Turn.all_reserved_date(self.food_center_1.id, self.day_datetime.date()), [])
            self.turn_one.save()
            self.assertEqual(Turn.all_reserved_date(self.food_center_1.id, self.day_datetime.date()), [self.turn_one])
            turn_two = Turn(
                email="juan@gmail.com",
                day_hour=self.day_datetime + timedelta(hours=1),
                donor_phone_number="2214053283",
                help_center=self.food_center_1
            )
            turn_two.save()
            self.assertEqual(Turn.all_reserved_date(self.food_center_1.id, self.day_datetime.date()), [self.turn_one, turn_two])

    

    def create_center_type(self):
        self.food_center_type = HelpCenterType(name="Centro de Alimentos")
        self.clothing_center_type = HelpCenterType(name="Centro de Ropa")
        self.blood_center_type = HelpCenterType(name="Centro de Sangre")

    def create_help_centers(self):
        self.food_center_1 = HelpCenter(
            name="Centro el Arroz",
            address="Av 64 e40 y 41 nro 30",
            phone_number="+54 294 412-3456",
            opening_time=time(9),
            closing_time=time(16),
            center_type=self.food_center_type,
            town=self.town_1,
            web_url="https://arroz.centro.org",
            email="arroz@centro.org"
        )