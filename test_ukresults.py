import pytest
from bs4 import BeautifulSoup as bs
from datetime import date

import ukresults as ukr
import result

"""
get_races scenarios
1. we're in Dec and want Nov and Dec
    just one index page
2. we're in Dec and want Jan - Dec
    just one index page
3. we're in Jan and want the whole of last year
    get last year's index page
4. we're in Jan and want Dec last year and Jan this year
    get Dec from last year's index page
    get Jan from this year's index page

https://www.ukresults.net/2021/index.html
https://www.ukresults.net/2022/index.html
"""



@pytest.fixture()
def index_page():
    with open('test-pages/ukresults/index_2021.html', "r") as file:
        return file.read()


def test_get_races(index_page):
    races = ukr.get_races(index_page, date.fromisoformat('2021-01-01'))
    assert len(races) == 109  # add assertion here

def test_get_selection_of_races(index_page):
    races = ukr.get_races(page, date.fromisoformat('2021-10-01'))
    assert len(races) == 34  # add assertion here


def test_year_urls():
    from_date = date.fromisoformat('2020-11-01')
    to_date = date.fromisoformat('2021-01-01')
    urls = []
    for year in range(from_date.year,to_date.year + 1):
        url = f"https://base_url/{year}/index.html"
        urls.append(url)
    assert len(urls) == 2
    assert urls[0] == 'https://base_url/2020/index.html'
