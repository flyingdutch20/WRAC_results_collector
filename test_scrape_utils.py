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


if __name__ == '__main__':
    unittest.main()
