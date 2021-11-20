from bs4 import BeautifulSoup
from datetime import date
import logging

import result
import scrape_utils as utils


logger = logging.getLogger("Results.racebest")


def correct_period(bs_table, from_date):
    header = bs_table.find("caption").text.split()
    if len(header) = 2:
        year = header[1]
        month = utils.lookup_month_index_from_abbr(header[0][0:3])
        table_date = date.fromisoformat(f"{year}-{month:0>2}-01")
    else:
        table_date = date.today()
    return table_date >= date.fromisoformat(f"{from_date.year}-{from_date.month:0>2}-01")


def extract_race(bs_table, from_date):
    rows = bs_table.findAll("tr")
    for row in rows:
        bs_row = BeautifulSoup


def get_index(base_url, weeks):
    index = []
    from_date = utils.find_from_date(weeks)
    bs = BeautifulSoup(utils.getpage(base_url, "racebest index"), "html.parser")
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
    index = get_index(base_url, weeks)
    for race_url in index:
        results.extend(get_results(race_url))
    return results
