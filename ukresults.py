from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as scr_utils

logger = logging.getLogger("Results.ukresults")

def get_results(line, base_url, test):
    pass


def get_races(page, from_date):
    pass


def collect_result(base_url, weeks, test):
    results = []
    logger.info("Retrieving the index page ...")
    #work out the year(s)
    from_date = scr_utils.find_from_date(weeks, date.today())
    for year in range(from_date.year,date.today().year):
        page = scr_utils.getpage(f"{base_url}/{year}/index.html", "racebest index")
        if page:
            races = get_races(page, from_date)
            logger.info(f"Retrieving the individual race pages; {len(races)} in total")
            for line in races:
                my_result = get_results(line, base_url, test)
                results.extend(my_result) if my_result else None
    return results
