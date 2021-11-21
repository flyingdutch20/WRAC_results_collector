from bs4 import BeautifulSoup
from datetime import date
import logging

import result
import scrape_utils as utils


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
    result = []
    rows = bs_table.findAll("tr")
    for row in rows:
        bs_row = BeautifulSoup(row, "html.parser")
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
            result.append(race)
    return result

def get_index(page, from_date):
    index = []
    bs = BeautifulSoup(page, "html.parser")
    months = bs.findAll("table", {"class": "table-bordered"})
    for table in months:
        bs_table = BeautifulSoup(table, "html.parser")
        if correct_period(bs_table, from_date):
            index.extend(extract_race(bs_table, from_date))
    return index


def get_results(race_url):
    results = []
    return results


def collect_result(base_url, weeks):
    results = []
    page = utils.getpage(base_url, "racebest index")
    from_date = utils.find_from_date(weeks, date.today())
    index = get_index(page, from_date)
    for line in index:
        results.extend(get_results(line))
    return results
