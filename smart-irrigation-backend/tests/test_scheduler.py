import unittest
import asyncio
from app.scheduler import schedule_for_field

class TestScheduler(unittest.TestCase):
    def test_schedule_logic(self):
        field = {
            "id": 1,
            "area_m2": 1000,
            "soil_type": "loamy",
            "crop_type": "wheat",
            "crop_stage": "vegetative",
            "irrigation_method": "sprinkler"
        }
        
        # Since schedule_for_field is async, we need to run it in an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(schedule_for_field(field, days=3))
        loop.close()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["status"], "scheduled")

if __name__ == '__main__':
    unittest.main()
