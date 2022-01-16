from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as scr_utils

logger = logging.getLogger("Results.ukresults")

def get_results(line, base_url, test):
    results = []
    return results

def parse_race_row(row, year, from_date, to_date, base_url):
    '"<tr><td>05 April</td><td><a href="fast5kapra.html"><b>Fast 5k Races, Three Sisters Circuit, Wigan, Lancashire</b></a></td></tr>"'
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    try:
        date_split = row.find("td").text.split(" ")
        a = row.find("a")
        link = a['href']
        name = a.text
        #create date
        day = date_split[0][0:2]
        month = months.index(date_split[1]) + 1
        race_date = date.fromisoformat(f"{year}-{month:02d}-{day}")
        if from_date <= race_date <= to_date:
            race = result.Race()
            race.date = race_date
            race.event = name
            race.url = f"{base_url}/{year}/{link}"
            return race
    except:
        return None

def get_races(page, year, from_date, to_date, base_url):
    races = []
    bs = BeautifulSoup(page, "html.parser")
    try:
        rows = bs.findAll("tr")
        for row in rows:
            race = parse_race_row(row, year, from_date, to_date, base_url)
            if race:
                races.append(race)
    except:
        None
    return races


def get_index_page_urls(base_url, from_date, to_date):
    urls = []
    for year in range(from_date.year, to_date.year + 1):  # range excludes last number
        urls.append((year, f"{base_url}/{year}/index.html"))
    return urls


def collect_result(base_url, weeks, test):
    results = []
    logger.info("Retrieving the index page(s) ...")
    to_date = date.today()
    from_date = scr_utils.find_from_date(weeks, to_date)
    index_page_urls = get_index_page_urls(from_date, to_date)
    for url in index_page_urls:
        year = url[0]
        page = scr_utils.getpage(url[1], f"ukresults index {year}")
        if page:
            races = get_races(page, year, from_date, to_date, base_url)
            logger.info(f"Retrieving the individual race pages; {len(races)} in total")
            for race in races:
                my_result = get_results(race, base_url, test)
                results.extend(my_result) if my_result else None
    return results
