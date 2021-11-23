import unittest
from datetime import date
import racebest as rb


class MyTestCase(unittest.TestCase):
    def test_get_index(self):
        with open('test-pages/racebest/index.html', "r") as file:
            page = file.read()
        index = rb.get_index(page, date.fromisoformat('2021-05-01'))
        self.assertEqual(18, len(index))  # add assertion here

    def test_get_runners(self):
        with open('test-pages/racebest/result_run.html', "r") as file:
            page = file.read()
        runners = rb.parse_race(page)
        self.assertEqual(158, len(runners))  # add assertion here

    def test_get_tri_runners(self):
        with open('test-pages/racebest/result_tri.html', "r") as file:
            page = file.read()
        tri_runners = rb.parse_race(page)
        self.assertEqual(107, len(tri_runners))  # add assertion here


if __name__ == '__main__':
    unittest.main()
