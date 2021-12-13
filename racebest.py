from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as utils
import racebest_utils as rb_utils

logger = logging.getLogger("Results.racebest")


def correct_period(bs_table, from_date):
    header = bs_table.find("caption").text.split()
    if (len(header) == 2):
        year = header[1]
        month = utils.lookup_month_index_from_abbr(header[0][0:3])
        table_date = date.fromisoformat(f"{year}-{month:0>2}-01")
    else:
        table_date = date.today()
    return table_date >= date.fromisoformat(f"{from_date.year}-{from_date.month:0>2}-01")


def extract_race(bs_table, from_date):
    races = []
    rows = bs_table.findAll("tr")
    for bs_row in rows:
        fields = bs_row.findAll("td")
        if len(fields) == 5:
            #todo parse date and test if after from_date
            race = result.Race()
            race.date = fields[0].text
            race.event = fields[1].text
            race.url = fields[1].find("a").get("href")
            race.location = fields[2].text
            race.distance = fields[3].text
            race.type = fields[4].text
            races.append(race)
    return races

def get_races(page, from_date):
    races = []
    bs = BeautifulSoup(page, "html.parser")
    months = bs.findAll("table", {"class": "table-bordered"})
    for bs_table in months:
        if correct_period(bs_table, from_date):
            races.extend(extract_race(bs_table, from_date))
    return races

def extract_header_fields(headerrow):
    headers = headerrow.findAll("th")
    my_fields = []
    for header in headers:
        spans = header.findAll("span")
        my_text = header.text if len(spans) < 2 else spans[1].text
        my_fields.append(my_text)
    return my_fields


def find_indices_from_header_fields(header_fields):
    result = {}
    result['pos'] = 0 if 'pos' in header_fields[0].lower() else None
    bib = re.compile('(B|b)ib')
    for field in header_fields:
         if bib.search(field):
             result["bib"] = header_fields[field]
    bib = re.compile('(R|r)ace (N|n)umber')
    for field in header_fields:
         if bib.search(field):
             result["bib"] = header_fields[field]
    name = re.compile('(N|n)ame')
    for field in header_fields:
         if name.search(field):
             result["name"] = header_fields[field]
    club = re.compile('(C|c)lub')
    for field in header_fields:
         if club.search(field):
             result["club"] = header_fields[field]
    gender = re.compile('(G|g)ender|(S|s)ex')
    for field in header_fields:
         if gender.search(field):
             result["gender"] = header_fields[field]
    category = re.compile('(C|c)ategory')
    position = re.compile('(P|p)osition')
    for field in header_fields:
         if category.search(field) and not position.search(field):
             result["catogry"] = header_fields[field]
#Time, Net Time, Finish Time, Gun Time

def create_field_index_from_header(headerrow, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    header_fields = extract_header_fields(headerrow)
    if test:
        rb_utils.store_header(header_fields)
    field_index = find_indices_from_header_fields(header_fields)
    return field_index

def create_runner(race, field_index, fields, test):
    return result.Result()

def parse_race(page, race, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    runners = []
    bs = BeautifulSoup(page, "html.parser")
    try:
        bs_table = bs.find("table", {"class": "results"})
        rows = bs_table.findAll("tr")
        field_index = create_field_index_from_header(rows[0], test)
        for bs_row in rows:
            fields = bs_row.findAll("td")
            runner = create_runner(race, field_index, fields, test)
            runners.append(runner) if runner is not None else None
    except:
        None
    return runners

def get_results(race, base_url, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    url = base_url + race.url
    page = utils.getpage(url, f"racebest race {race.event}")
    if page:
        runners = parse_race(page, race, test)
        return runners

def collect_result(base_url, weeks, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    results = []
    page = utils.getpage(base_url + '/results', "racebest index")
    if page:
        from_date = utils.find_from_date(weeks, date.today())
        races = get_races(page, from_date)
        for line in races:
            my_result = get_results(line, base_url, test)
            results.extend(my_result) if my_result else None
        return results
