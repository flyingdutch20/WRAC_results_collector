import pytest
from bs4 import BeautifulSoup as bs
from datetime import date

import ukresults as ukr
import result



headerrow = '<th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Pos<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Num<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">M<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">F<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Name<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Cat<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">CatPos<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Club<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">ChipTime<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">ChipPos<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">Pace per Km/Mile<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th><th><a href="#" class="sortheader" onclick="ts_resortTable(this);return false;">GunTime<span class="sortarrow">&nbsp;&nbsp;&nbsp;</span></a></th></tr>'


def test_create_field_index_from_header():
    row = bs(headerrow, 'html.parser')
    fields = ukr.create_field_index_from_header(row)
    assert len(fields) == 9

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
5. we're in Apr and want the wole of last year, July - Dec of the year before and the first 3 months of this year
    get the the last 6 months of the year before last
    get the whole of last year
    get the first 3 months of this year
https://www.ukresults.net/2021/index.html
https://www.ukresults.net/2022/index.html
"""



def test_parse_race_line():
    line = '<tr><td>05 April</td><td><a href="fast5kapra.html"><b>Fast 5k Races, Three Sisters Circuit, Wigan, Lancashire</b></a></td></tr>'
    bs_line = bs(line, "html.parser")
    my_race = ukr.parse_race_row(bs_line, 2021, date.fromisoformat("2021-01-01"), date.fromisoformat("2021-12-31"), "/base_url")
    assert my_race.date == date.fromisoformat("2021-04-05")
    assert my_race.url == "/base_url/2021/fast5kapra.html"
    assert my_race.event == "Fast 5k Races, Three Sisters Circuit, Wigan, Lancashire"


@pytest.fixture()
def index_page_2021():
    with open('test-pages/ukresults/index_2021.html', "r") as file:
        return file.read()

@pytest.fixture()
def index_page_2022():
    with open('test-pages/ukresults/index_2022.html', "r") as file:
        return file.read()

def test_get_races(index_page_2022):
    year = 2022
    base_url = "base_url"
    from_date = date.fromisoformat('2022-01-01')
    to_date = date.fromisoformat('2022-01-31')
    races = ukr.get_races(index_page_2022, year, from_date, to_date, base_url)
    assert len(races) == 4

def test_get_selection_of_races(index_page_2021):
    year = 2021
    base_url = "base_url"
    races = ukr.get_races(index_page_2021, year, date.fromisoformat('2021-10-01'), date.fromisoformat('2021-12-31'), base_url)
    assert len(races) == 34  # add assertion here

def test_get_index_pages():
    page_urls = ukr.get_index_page_urls('base_url',date.fromisoformat('2021-11-01'),date.fromisoformat('2021-12-31'))
    assert len(page_urls) == 1
    page_urls = ukr.get_index_page_urls('base_url',date.fromisoformat('2021-01-01'),date.fromisoformat('2021-12-31'))
    assert len(page_urls) == 1
    page_urls = ukr.get_index_page_urls('base_url',date.fromisoformat('2021-12-01'),date.fromisoformat('2022-01-16'))
    assert len(page_urls) == 2
    page_urls = ukr.get_index_page_urls('base_url',date.fromisoformat('2020-07-01'),date.fromisoformat('2022-03-31'))
    assert len(page_urls) == 3


def test_year_urls():
    from_date = date.fromisoformat('2020-11-01')
    to_date = date.fromisoformat('2021-01-01')
    urls = []
    for year in range(from_date.year,to_date.year + 1):
        url = f"https://base_url/{year}/index.html"
        urls.append(url)
    assert len(urls) == 2
    assert urls[0] == 'https://base_url/2020/index.html'
