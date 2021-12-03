from datetime import date
import pytest

import scrape_utils as su

"""
Test lookup_month_index_from_abbr
Input is string, output is month index as integer
If input is not in the lookup table, then return 1
If input is None, return error invalid input
If input is longer than 3 characters, use first 3 characters
Input and lookup should be case insensitive
"""

def test_lookup_month_index_from_abbr():
    with pytest.raises(TypeError):
        su.lookup_month_index_from_abbr()
    assert su.lookup_month_index_from_abbr('Jan') == 1
    assert su.lookup_month_index_from_abbr('') == 1
    assert su.lookup_month_index_from_abbr('aaa') == 1
    assert su.lookup_month_index_from_abbr('jun') == 6
    assert su.lookup_month_index_from_abbr('August') == 8

"""
Test find_from_date
Input is number of weeks (int) and date
Output is a date, the monday of the date minus the number of weeks
If number of weeks is 0, then return the monday of the same date
If number of weeks is negative or not a number, return an error
If date is not a date, return an error
Extra attention crossing one year (5 weeks back from January)
Extra attention crossing more than one year (60 weeks back from January)
Extra attention when there are 52 or 53 weeks in a year.
"""

@pytest.fixture()
def my_date():
    return date.fromisoformat("2021-02-02")

def test_find_from_date_1_week(my_date):
    outdate = su.find_from_date(1, my_date)
    testdate = date.fromisoformat("2021-01-25")
    assert  outdate == testdate

def test_find_from_date_jump_year(my_date):
    outdate = su.find_from_date(5, my_date)
    testdate = date.fromisoformat("2020-12-28")
    assert outdate == testdate
