from bs4 import BeautifulSoup
from datetime import date
import logging
import re

import result
import scrape_utils as scr_utils
import racebest_utils as rb_utils

logger = logging.getLogger("Results.racebest")


def correct_period(bs_table, from_date):
    header = bs_table.find("caption").text.split()
    if (len(header) == 2):
        year = header[1]
        month = scr_utils.lookup_month_index_from_abbr(header[0][0:3])
        table_date = date.fromisoformat(f"{year}-{month:0>2}-01")
    else:
        table_date = date.today()
    return table_date >= date.fromisoformat(f"{from_date.year}-{from_date.month:0>2}-01")


def extract_races_in_month_table(bs_table, from_date):
    races = []
    rows = bs_table.findAll("tr")
    for bs_row in rows:
        fields = bs_row.findAll("td")
        if len(fields) == 5:
            race = result.Race()
            #todo parse date and test if after from_date
            race.date = fields[0].text
            race.event = fields[1].find("a").text
            race.url = fields[1].find("a").get("href")
            race.location = fields[2].text
            race.distance = fields[3].text
            race.type = fields[4].text
            if race.url:
                #logger.info(f"Found and extracted race {race.event} - {race.date}")
                races.append(race)
    return races

def get_races(page, from_date):
    races = []
    logger.info("Parsing the index page to extract the individual races")
    bs = BeautifulSoup(page, "html.parser")
    months = bs.findAll("table", {"class": "table-bordered"})
    #logger.info(f"Found {len(months)} months")
    for bs_table in months:
        if correct_period(bs_table, from_date):
            month_races = extract_races_in_month_table(bs_table, from_date)
            races.extend(month_races)
    return races

def extract_header_fields(headerrow):
    try:
        headers = headerrow.findAll("th")
    except Exception as error:
        raise error
    my_fields = []
    for header in headers:
        spans = header.findAll("span")
        my_text = header.text if len(spans) < 2 else spans[1].text
        my_fields.append(my_text) if my_text else None
    return my_fields


def find_bib_index(header_fields):
    index = None
    bib = re.compile('bib',flags=re.I)
    bibnum = re.compile('bib number',flags=re.I)
    rnum = re.compile('race number',flags=re.I)
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


def find_gender_index(header_fields):
    index = None
    gender = re.compile('gender',flags=re.I)
    sex = re.compile('sex',flags=re.I)
    for field in header_fields:
        if gender.fullmatch(field):
            index = header_fields.index(field)
            break
        elif sex.fullmatch(field):
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
    chip = re.compile('chip time',flags=re.I)
    net = re.compile('net time',flags=re.I)
    finish = re.compile('finish time',flags=re.I)
    tottime = re.compile('total time',flags=re.I)
    time = re.compile('time',flags=re.I)
    gun = re.compile('gun time',flags=re.I)
    keys = [chip,net,finish,tottime,time,gun]
    for key in keys:
        for field in header_fields:
            if key.fullmatch(field):
                index = header_fields.index(field)
                break
        if index:
            break
    return index


def find_swim_index(header_fields):
    index = None
    swim = re.compile('swim',flags=re.I)
    for field in header_fields:
        if swim.search(field):
            index = header_fields.index(field)
            break
    return index


def find_t1_index(header_fields):
    index = None
    t1 = re.compile('t1',flags=re.I)
    for field in header_fields:
        if t1.search(field):
            index = header_fields.index(field)
            break
    return index


def find_bike_index(header_fields):
    index = None
    bike = re.compile('bike',flags=re.I)
    for field in header_fields:
        if bike.search(field):
            index = header_fields.index(field)
            break
    return index


def find_t2_index(header_fields):
    index = None
    t2 = re.compile('t2',flags=re.I)
    for field in header_fields:
        if t2.search(field):
            index = header_fields.index(field)
            break
    return index


def find_run_index(header_fields):
    index = None
    run = re.compile('run',flags=re.I)
    for field in header_fields:
        if run.search(field):
            index = header_fields.index(field)
            break
    return index


def find_indices_from_header_fields(header_fields):
    assert isinstance(header_fields,list)
    result = {}
    result['pos'] = 0 if header_fields and 'pos' in header_fields[0].lower() else None
    result['bib'] = find_bib_index(header_fields)
    result['name'] = find_name_index(header_fields)
    result['club'] = find_club_index(header_fields)
    result['gender'] = find_gender_index(header_fields)
    result['category'] = find_category_index(header_fields)
    result['time'] = find_time_index(header_fields)
    # 10. if Triathlon: Swim,T1,Bike,T2,Run,Finish Time/Swim Incl Run,T1,Bike,T2,Run,Time,
    result['swim'] = find_swim_index(header_fields)
    result['t1'] = find_t1_index(header_fields)
    result['bike'] = find_bike_index(header_fields)
    result['t2'] = find_t2_index(header_fields)
    result['run'] = find_run_index(header_fields)
    return result

def create_field_index_from_header(headerrow, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    header_fields = extract_header_fields(headerrow)
    if test:
        rb_utils.store_header(header_fields)
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
    return runner

def parse_race(page, race, test=False):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    runners = []
    bs = BeautifulSoup(page, "html.parser")
    all_text = bs.text
    wr = re.compile('wrac|wetherby', flags=re.I)
    if wr.search(all_text):
        logger.info(f"Race {race.event} has Wetherby Runners participants")
        try:
            bs_table = bs.find("table", {"class": "results"})
            rows = bs_table.findAll("tr")
            field_index = create_field_index_from_header(rows[0], test)
            if field_index['club']:
                # if no club then no point in parsing
                for bs_row in rows:
                    fields = bs_row.findAll("td")
                    if fields:
                        runner = create_runner(race, field_index, fields, test)
                        if runner is not None and wr.search(runner.club):
                            runners.append(runner)
        except:
            None
    return runners

def get_results(race, base_url, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    url = base_url + race.url
    page = scr_utils.getpage(url, f"racebest race {race.event}")
    if page:
        #logger.info(f"Parsing {race.event} - {race.date}")
        runners = parse_race(page, race, test)
        return runners

def collect_result(base_url, weeks, test):
    #the test parameter will extract bits of the pages and store them on disk as test sets
    results = []
    logger.info("Retrieving the index page ...")
    page = scr_utils.getpage(base_url + '/results', "racebest index")
    if page:
        from_date = scr_utils.find_from_date(weeks, date.today())
        races = get_races(page, from_date)
        logger.info(f"Retrieving the individual race pages; {len(races)} in total")
        for line in races:
            my_result = get_results(line, base_url, test)
            results.extend(my_result) if my_result else None
    return results
