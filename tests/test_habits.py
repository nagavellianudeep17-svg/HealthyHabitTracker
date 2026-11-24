import unittest
from validation import validate_record
from habit_engine import make_record,filter_records,weekly_summary
from datetime import date

class HabitTrackerTests(unittest.TestCase):
    def test_valid_record(self):
        self.assertEqual(validate_record("2026-11-23","Reading","30"),[])
    def test_bad_date(self):
        self.assertTrue(validate_record("23-11-2026","Reading","30"))
    def test_negative_amount(self):
        self.assertTrue(validate_record("2026-11-23","Exercise","-5"))
    def test_hydration_limit(self):
        self.assertTrue(validate_record("2026-11-23","Hydration","21"))
    def test_record_created(self):
        r=make_record("2026-11-23","Reading","25","test")
        self.assertEqual(r["habit"],"Reading")
    def test_filter_keyword(self):
        r=make_record("2026-11-23","Reading","25","novel")
        self.assertEqual(len(filter_records([r],keyword="novel")),1)
if __name__=="__main__":unittest.main()
