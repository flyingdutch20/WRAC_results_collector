import unittest
from datetime import date

import scrape_utils as su

class MyTestCase(unittest.TestCase):
    def test_find_from_date_1_week(self):
        mydate = date.fromisoformat("2021-02-02")
        outdate = su.find_from_date(1,mydate)
        testdate = date.fromisoformat("2021-01-25")
        self.assertEqual(testdate, outdate)  # add assertion here

    def test_find_from_date_jump_year(self):
        mydate = date.fromisoformat("2021-01-12")
        outdate = su.find_from_date(2,mydate)
        testdate = date.fromisoformat("2020-12-28")
        self.assertEqual(testdate, outdate)  # add assertion here

    def test_lookup_month_index_apr(self):
        output = su.lookup_month_index_from_abbr("Apr")
        self.assertEqual(4,output)

    def test_lookup_month_index_blank(self):
        output = su.lookup_month_index_from_abbr("")
        self.assertEqual(1, output)

    def test_seconds_from_timestring_hhmmss(self):
        seconds = su.seconds_from_timestring("01:01:01")
        self.assertEqual(3661, seconds)
        seconds = su.seconds_from_timestring("01.01.01")
        self.assertEqual(3661, seconds)

    def test_seconds_from_timestring_mmss(self):
        seconds = su.seconds_from_timestring("61:01")
        self.assertEqual(3661, seconds)
        seconds = su.seconds_from_timestring("15.12")
        self.assertEqual(912, seconds)


if __name__ == '__main__':
    unittest.main()
