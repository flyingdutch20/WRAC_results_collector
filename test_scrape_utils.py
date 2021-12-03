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

def test_find_from_date_input_errors(my_date):
    with pytest.raises(TypeError):
        su.find_from_date()
    with pytest.raises(TypeError):
        su.find_from_date(None, my_date)
    with pytest.raises(AssertionError):
        su.find_from_date(1, None)
    with pytest.raises(AssertionError):
        su.find_from_date(-1, my_date)
    with pytest.raises(AssertionError):
        su.find_from_date(1, "15-Jan-2021")

def test_find_from_date_1_week(my_date):
    outdate = su.find_from_date(1, my_date)
    testdate = date.fromisoformat("2021-01-25")
    assert  outdate == testdate

def test_find_from_date_jump_year(my_date):
    outdate = su.find_from_date(5, my_date)
    testdate = date.fromisoformat("2020-12-28")
    assert outdate == testdate

def test_find_from_date_same_week(my_date):
    outdate = su.find_from_date(0, my_date)
    testdate = date.fromisoformat("2021-02-01")
    assert outdate == testdate

def test_find_from_date_jump_full_year(my_date):
    outdate = su.find_from_date(57, my_date)
    testdate = date.fromisoformat("2019-12-30")
    assert outdate == testdate

"""
Test seconds_from_timestring
Input is a string that represents the elapsed time. This can be a number of minutes and seconds
or a number of hours, minutes and seconds or just seconds and possibly even days, hours, minutes, seconds. 
Different separators are used; ":.' (space)"
Output is the total seconds as an integer
"""

def test_seconds_from_timestring_bad_input():
    assert su.seconds_from_timestring("ab'ab'ab") == 0
    assert su.seconds_from_timestring("01'01abc01") == 0

def test_seconds_from_timestring_hhmmss():
    assert su.seconds_from_timestring("01:01:01") == 3661
    assert su.seconds_from_timestring("01.01.01") == 3661
    assert su.seconds_from_timestring("01'01 01") == 3661
    assert su.seconds_from_timestring("01.012.01") == 4321

def test_seconds_from_timestring_mmss():
    assert su.seconds_from_timestring("61:01") == 3661
    assert su.seconds_from_timestring("15.12") == 912
    assert su.seconds_from_timestring("101:01") == 6061

def test_seconds_from_timestring_dhhmmss():
    assert su.seconds_from_timestring("01:01:01:01") == 90061
    assert su.seconds_from_timestring("01d01h01m01s") == 90061
