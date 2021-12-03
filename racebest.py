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


def parse_race(page, race):
    runners = []
    bs = BeautifulSoup(page, "html.parser")
    bs_table = bs.find("table", {"class": "results"})
    rows = bs_table.findAll("tr")
    for bs_row in rows:
        fields = bs_row.findAll("td")
        if len(fields) == 10: # running race
            #todo parse date and test if after from_date
            runner = result.Result()
            race = fields[0].text

    return runners

def get_results(race, base_url):
    url = base_url + '/' + race.url
    page = utils.getpage(url, f"racebest race {race.name}")
    runners = parse_race(page, race)
    return runners

def collect_result(base_url, weeks):
    results = []
    page = utils.getpage(base_url, "racebest index")
    from_date = utils.find_from_date(weeks, date.today())
    races = get_races(page, from_date)
    for line in races:
        results.extend(get_results(line, base_url))
    return results
