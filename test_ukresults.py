import pytest
from bs4 import BeautifulSoup as bs
from datetime import date

import ukresults as ukr
import result


@pytest.fixture()
def index_page():
    with open('test-pages/ukresults/index.html', "r") as file:
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
