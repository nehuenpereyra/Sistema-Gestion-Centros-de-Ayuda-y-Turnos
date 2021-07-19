
from datetime import datetime, time, timedelta

from . import BaseTestClass 

from app.models.help_center import HelpCenter
from app.models.help_center_type import HelpCenterType
from app.models.town import Town
from app.models.town_phase import TownPhase
from app.models.turn import Turn

class HelpCenterTest(BaseTestClass):
    """Help Center model test suite"""

    def setUp(self):
        super().setUp()

        self.food_center_type = HelpCenterType(name="Centro de Alimentos")
        self.clothing_center_type = HelpCenterType(name="Centro de Ropa")
        self.blood_center_type = HelpCenterType(name="Centro de Sangre")

        self.town_phase_1 = TownPhase(id=0, title="")

        self.town_1 = Town(
            id=0,
            name="",
            phase=self.town_phase_1
        )

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

        self.food_center_2 = HelpCenter(
            name="Centro la Papa",
            address="Av 80 e20 y 21 nro 90",
            phone_number="+54 294 410-2030",
            opening_time=time(9),
            closing_time=time(16),
            center_type=self.food_center_type,
            town=self.town_1,
            web_url="https://papa.centro.org",
            email="papa@centro.org",
            request_status=True
        )

        self.clothing_center = HelpCenter(
            name="Centro la Camisa",
            address="Av 20 e42 y 43 nro 64",
            phone_number="+54 294 420-2040",
            opening_time=time(9),
            closing_time=time(16),
            center_type=self.clothing_center_type,
            town=self.town_1,
            web_url="https://camisa.centro.org",
            email="camisa@centro.org",
            request_status=False)

        self.blood_center = HelpCenter(
            name="Centro la Gota",
            address="Av 46 e80 y 81 nro 70",
            phone_number="+54 294 440-2010",
            opening_time=time(9),
            closing_time=time(16),
            center_type=self.blood_center_type,
            town=self.town_1,
            web_url="https://gota.centro.org",
            published=False,
            request_status=True)

        self.turn_one = Turn(
            email="juan@gmail.com",
            day_hour=datetime.now() + timedelta(hours=2),
            donor_phone_number="2214053283",
            help_center=self.food_center_2
        )

        self.turn_two = Turn(
            email="ramiro@gmail.com", 
            day_hour=datetime.now() - timedelta(days=7),
            donor_phone_number="2214053283",
            help_center=self.food_center_2
        )

        self.turn_three = Turn(
            email="julieta@gmail.com",
            day_hour=datetime.now() - timedelta(days=2),
            donor_phone_number="2214053283",
            help_center=self.food_center_2,
            name="Julieta",
            surname="Filpin"
        )

        self.turn_four = Turn(
            email="marcela@gmail.com",
            day_hour=datetime.now() - timedelta(hours=1),
            donor_phone_number="2214053283",
            help_center=self.blood_center
        )
    
    def test_get(self):
        with self.app.app_context():
            self.assertIsNone(HelpCenter.get(2000))
            self.food_center_2.save()
            self.blood_center.save()
            self.assertEqual(HelpCenter.get(self.food_center_2.id), self.food_center_2)
            self.assertEqual(HelpCenter.get(self.blood_center.id), self.blood_center)
    
    def test_get_public_center(self):
        with self.app.app_context():
            self.assertIsNone(HelpCenter.get_public_center(2000))
            self.food_center_1.save()
            self.food_center_2.save()
            self.blood_center.save()
            self.assertIsNone(HelpCenter.get_public_center(self.food_center_1.id))
            self.assertEqual(HelpCenter.get_public_center(self.food_center_2.id), self.food_center_2)
            self.assertIsNone(HelpCenter.get_public_center(self.blood_center.id))
    
    def test_save(self):
        with self.app.app_context():
            self.assertEqual(HelpCenter.get_by_name(self.food_center_2.name), [])
            self.food_center_2.save()
            self.assertEqual(HelpCenter.get_by_name(self.food_center_2.name), [self.food_center_2])
        
    def test_remove(self):
        with self.app.app_context():
            self.food_center_2.save()
            self.assertEqual(HelpCenter.get_by_name(self.food_center_2.name), [self.food_center_2])
            self.food_center_2.remove()
            self.assertEqual(HelpCenter.get_by_name(self.food_center_2.name), [])

    def test_is_in_pending_state(self):
        with self.app.app_context():
            self.assertFalse(self.food_center_2.is_in_pending_state())
            self.assertFalse(self.clothing_center.is_in_pending_state())
            self.assertTrue(self.food_center_1.is_in_pending_state())
            
    def test_is_in_rejected_state(self):
        with self.app.app_context():
            self.assertFalse(self.food_center_2.is_in_rejected_state())
            self.assertTrue(self.clothing_center.is_in_rejected_state())
            self.assertFalse(self.food_center_1.is_in_rejected_state())
        
    def test_is_in_accepted_state(self):
        with self.app.app_context():
            self.assertTrue(self.food_center_2.is_in_accepted_state())
            self.assertFalse(self.clothing_center.is_in_accepted_state())
            self.assertFalse(self.food_center_1.is_in_accepted_state())
        
    def test_accept_request(self):
        with self.app.app_context():
            self.assertTrue(self.food_center_1.is_in_pending_state())
            self.food_center_1.accept_request()
            self.assertTrue(self.food_center_1.is_in_accepted_state())
        
    def test_reject_request(self):
        with self.app.app_context():
            self.assertTrue(self.food_center_1.is_in_pending_state())
            self.food_center_1.reject_request()
            self.assertTrue(self.food_center_1.is_in_rejected_state())
    
    def test_has_turn(self):
        with self.app.app_context():
            self.assertTrue(self.food_center_2.has_turn(self.turn_one))
            self.assertFalse(self.blood_center.has_turn(self.turn_one))

            self.assertTrue(self.blood_center.has_turn(self.turn_four))
            self.assertFalse(self.clothing_center.has_turn(self.turn_four))

    def test_all_published(self):
        with self.app.app_context():
            self.assertEqual(HelpCenter.all_published(), ([], 0))
            
            self.food_center_1.save()
            self.food_center_2.save()
            self.clothing_center.save()
            self.blood_center.save()

            self.assertEqual(HelpCenter.all_published(), ([self.food_center_2], 1))

    def test_get_with_more_turns(self):
        with self.app.app_context():
            self.food_center_1.save()
            self.food_center_2.save()
            self.blood_center.save()
            
            self.assertEqual(HelpCenter.get_with_more_turns(0), [])
            self.assertEqual(HelpCenter.get_with_more_turns(2), [
                self.food_center_2,
                self.blood_center
            ])
            self.assertEqual(HelpCenter.get_with_more_turns(10), [
                self.food_center_2,
                self.blood_center,
                self.food_center_1
            ])

    def test_has_pending_turns(self):
        with self.app.app_context():
            self.assertFalse(self.food_center_1.has_pending_turns())
            self.assertTrue(self.food_center_2.has_pending_turns())
            self.assertFalse(self.clothing_center.has_pending_turns())
            self.assertFalse(self.blood_center.has_pending_turns())

    """ def test_search(self):
        with self.app.app_context():
            pass
        
    def test_reserve_turn(self):
        with self.app.app_context():
            pass
    
    """