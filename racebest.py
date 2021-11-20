from bs4 import BeautifulSoup
from datetime import date
import logging

import result
import scrape_utils as utils


logger = logging.getLogger("Results.racebest")


def get_index(base_url, weeks):
    index = []
    to_date = date.today()
    from_date = utils.find_from_date(weeks)
    bs = BeautifulSoup(utils.getpage(base_url, "racebest index"), "html.parser")
    months = bs.findAll("table", {"class": "table-bordered"})
    for table in months:
        pass
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
