from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as scr_utils
#import runbritain_utils as rb_utils

logger = logging.getLogger("Results.runbritain")


def get_results(race, base_url, test):
    results = []
    return results


def get_races(page, from_date):
    races = []
    # /results.aspx?meetingid=443321
    return races


def collect_result(base_url, weeks, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    results = []
    logger.info("Retrieving the index page ...")
    page = scr_utils.getpage(base_url + '/resultslookup.aspx', "runbritain index")
    if page:
        from_date = scr_utils.find_from_date(weeks, date.today())
        races = get_races(page, from_date)
        logger.info(f"Retrieving the individual race pages; {len(races)} in total")
        for line in races:
            my_result = get_results(line, base_url, test)
            results.extend(my_result) if my_result else None
    return results
