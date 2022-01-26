from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as scr_utils
import result_utils as res_utils

logger = logging.getLogger("Results.ukresults")

def find_bib_index(header_fields):
    index = None
    bib = re.compile('bib',flags=re.I)
    bibnum = re.compile('bib number',flags=re.I)
    rnum = re.compile('race number',flags=re.I)
    num = re.compile('num',flags=re.I)
    for field in header_fields:
        if bib.fullmatch(field):
            index = header_fields.index(field)
            break
        elif bibnum.fullmatch(field):
            index = header_fields.index(field)
            break
        elif rnum.fullmatch(field):
            index = header_fields.index(field)
            break
        elif num.fullmatch(field):
            index = header_fields.index(field)
            break
    return index


def find_name_index(header_fields):
    index = None
    name = re.compile('name',flags=re.I)
    for field in header_fields:
        if name.fullmatch(field):
            index = header_fields.index(field)
            break
    return index


def find_club_index(header_fields):
    # 11. find 'Club', 'Club / Sponsor', 'Club Name', 'Team', 'Team Name'. If both Club and Team then Club prevails
    index = None
    club = re.compile('club',flags=re.I)
    team = re.compile('team',flags=re.I)
    cname = re.compile('club name',flags=re.I)
    tname = re.compile('team name',flags=re.I)
    for field in header_fields:
        if club.fullmatch(field):
            index = header_fields.index(field)
            break
        elif team.fullmatch(field):
            index = header_fields.index(field)
            break
        elif cname.fullmatch(field):
            index = header_fields.index(field)
            break
        elif tname.fullmatch(field):
            index = header_fields.index(field)
            break
    if not index:
        for field in header_fields:
            if club.search(field):
                index = header_fields.index(field)
                break
            elif team.search(field):
                index = header_fields.index(field)
                break
    return index


def find_male_index(header_fields):
    index = None
    male = re.compile('m',flags=re.I)
    for field in header_fields:
        if male.fullmatch(field):
            index = header_fields.index(field)
            break
    return index


def find_female_index(header_fields):
    index = None
    female = re.compile('f',flags=re.I)
    for field in header_fields:
        if female.fullmatch(field):
            index = header_fields.index(field)
            break
    return index


def find_category_index(header_fields):
    # 8. find 'Category', 'Cat', 'Age Category', 'Gender Category' make sure not 'Category Position'
    index = None
    category = re.compile('category', flags=re.I)
    cat = re.compile('cat', flags=re.I)
    agecat = re.compile('age category', flags=re.I)
    gencat = re.compile('gender category', flags=re.I)
    for field in header_fields:
        if category.fullmatch(field):
            index = header_fields.index(field)
            break
        elif cat.fullmatch(field):
            index = header_fields.index(field)
            break
        elif agecat.fullmatch(field):
            index = header_fields.index(field)
            break
        elif gencat.fullmatch(field):
            index = header_fields.index(field)
            break
    return index


def find_time_index(header_fields):
    # Time, Net Time, Finish Time, Chip Time, Gun Time
    # 9. find 'Time', 'TIME', 'Net Time', 'Finish Time', 'Chip Time'. If multiple, then order 'Chip Time', 'Net Time', 'Finish Time', 'Time'
    # triathlon: 'Total Time'
    index = None
    chip = re.compile('chip time|chiptime',flags=re.I)
    net = re.compile('net time|nettime',flags=re.I)
    finish = re.compile('finish time|finishtime',flags=re.I)
    tottime = re.compile('total time|totaltime',flags=re.I)
    time = re.compile('time',flags=re.I)
    gun = re.compile('gun time|guntime',flags=re.I)
    keys = [chip,net,finish,tottime,time,gun]
    for key in keys:
        for field in header_fields:
            if key.fullmatch(field):
                index = header_fields.index(field)
                break
        if index:
            break
    return index


def find_indices_from_header_fields(header_fields):
    assert isinstance(header_fields,list)
    result = {}
    result['pos'] = 0 if header_fields and 'pos' in header_fields[0].lower() else None
    result['bib'] = find_bib_index(header_fields)
    result['name'] = find_name_index(header_fields)
    result['club'] = find_club_index(header_fields)
    result['male'] = find_male_index(header_fields)
    result['female'] = find_female_index(header_fields)
    result['category'] = find_category_index(header_fields)
    result['time'] = find_time_index(header_fields)
    return result


def extract_header_fields(headerrow):
    try:
        headers = headerrow.findAll("th")
    except Exception as error:
        raise error
    my_fields = []
    for header in headers:
        my_text = header.text.strip()
        my_fields.append(my_text) if my_text else None
    return my_fields


def create_field_index_from_header(headerrow, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    header_fields = extract_header_fields(headerrow)
    if test:
        res_utils.store_ukresults_header(header_fields)
    field_index = find_indices_from_header_fields(header_fields)
    return field_index


def create_runner(race, field_index, fields, test):
    runner = result.Result()
    runner.date = race.date
    runner.race = race.event
    runner.distance = race.distance
    runner.racetype = race.type
    runner.location = race.location
    for key in field_index.keys():
        index = field_index[key]
        if index is not None:
            val = fields[index].text
            setattr(runner,key,val)
    if runner.pos == '1':
        race.winningtime = runner.time
    runner.winningtime = race.winningtime
    if runner.category[0] in 'MF':
        runner.gender = runner.category[0]
    return runner

def multi_races_page(bs, race, test):
    runners = []
    multi_races_tables = bs.findAll("table")
    if len(multi_races_tables) > 1:
        return runners
    race_rows = multi_races_tables[0].findAll("tr")
    single = True
    if len(race_rows) < 20:
        for row in race_rows:
            if len(row.findAll("td")) > 1:
                return runners
    for row in race_rows:
        try:
            a = row.find("a")
            link = a['href']
            name = a.text
            subrace = result.Race()
            subrace.url = link
            subrace.event = f"{race.event} - {name}"
            subrace.date = race.date
            subrace.year = race.year
            subrace.base_url = race.base_url
            subrace_results = get_results(subrace, test)
            runners.extend(subrace_results)
        except:
            None
    return runners

def parse_race(page, myrace, test):
    runners = []
    bs = BeautifulSoup(page, "html.parser")
    runners.append(multi_races_page(bs, myrace, test))
    all_text = bs.text
    wr = re.compile('wrac|wetherby', flags=re.I)
    if wr.search(all_text):
        logger.info(f"Race {myrace.event} has Wetherby Runners participants")
        try:
            bs_table = bs.find("table", {"class": "sortable"})
            rows = bs_table.findAll("tr")
            field_index = create_field_index_from_header(rows[0], test)
            if field_index['club']:
                # if no club then no point in parsing
                for bs_row in rows:
                    fields = bs_row.findAll("td")
                    if fields:
                        runner = create_runner(myrace, field_index, fields, test)
                        if runner is not None and wr.search(runner.club):
                            runners.append(runner)
        except:
            None
    return runners


def get_results(race, test):
    race_url = f"{race.base_url}/{race.year}/{race.url}"
    page = scr_utils.getpage(race_url, f"ukresults {race.event}")
    if page:
        # logger.info(f"Parsing {race.event} - {race.date}")
        runners = parse_race(page, race, test)
        return runners


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
            race.year = year
            race.base_url = base_url
            race.url = link
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
    index_page_urls = get_index_page_urls(base_url, from_date, to_date)
    for url in index_page_urls:
        year = url[0]
        page = scr_utils.getpage(url[1], f"ukresults index {year}")
        if page:
            races = get_races(page, year, from_date, to_date, base_url)
            logger.info(f"Retrieving the individual race pages; {len(races)} in total")
            for race in races:
                my_result = get_results(race, test)
                results.extend(my_result) if my_result else None
    return results
