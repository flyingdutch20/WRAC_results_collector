from bs4 import BeautifulSoup
from datetime import date
import os
import requests
import json
import pickle
import tote
import copy
import odds
import db
import logging
import re
import pp_value
import csv
import yaml

yaml_file = 'config.yml'
try:
    with open(yaml_file, 'r') as c_file:
      config = yaml.safe_load(c_file)
except Exception as e:
    print('Error reading the config file')
logs_dir = config['directories']['logs_dir']
meetings_dir = config['directories']['meetings_dir']
rp_base_url = config['urls']['rp_base_url']

if not os.path.isdir("./" + logs_dir):
    os.mkdir("./" + logs_dir)
logname = "./" + logs_dir + "/" + date.today().strftime('%Y-%m-%d') + "-pp.log"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename=logname,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger("Placepot.main")
logger.debug('Debug message should go to the log file')
logger.info('Info message to the console and the log file')
logger.warning('Warning message to the console and log file')
logger.error('Error message should go everywhere')


infile = open('courselist_tote.txt')
courselist_dict = {}
for line in infile.read().split("\n"):
    words = line.split()
    if len(words) > 1:
        courselist_dict[words[0].strip().lower()] = words[1].strip().lower()
    else:
        courselist_dict[words[0].strip().lower()] = words[0].strip().lower()


def read_racingpost_index(sel_mtg, collect_pp, results):
    bs = BeautifulSoup(getpage(rp_base_url, "rpindex"), "html.parser")
    raw_meetings = bs.findAll("section", {"class": "ui-accordion__row"})
    no_of_mtgs = 0
    for raw_mtg in raw_meetings:
        mtg = extract_rp_meeting(raw_mtg, sel_mtg)
        if mtg is not None:
            no_of_mtgs += 1
            mtg.collect_results(collect_pp, results)
            mtg.set_ppvalue()
            logger.info(f"Saving {mtg.name}")
            mtg.writemtg()
    logger.info(f"Saved {no_of_mtgs} meetings.")

def read_mtgs_from_directory(dir):
    result = []
    for entry in os.listdir(dir):
        my_file = os.path.join(dir, entry)
        if os.path.isfile(my_file):
            mtg = unpickle_mtg(my_file)
            result.append(mtg) if mtg is not None else None
    return result


def unpickle_mtg(filename):
    with open(filename, "rb") as mtgfile:
        mtg = None
        try:
            mtg = pickle.load(mtgfile)
        except Exception:
            logger.error(f"Can't unpickle {filename}")
        if isinstance(mtg, Meeting):
            logger.info(f"Meeting {mtg.name} - {mtg.race_date} loaded")
            return mtg
        else:
            return None


def getpage(url, name):
    r = requests.get(url)
    if r.status_code > 299:
        logger.warning(f"No results available for {name}")
        return ""
    html = r.text
    return html


def find_or_empty(bs, key, search):
    if bs is None:
        return ""
    s = bs.find(key, {"class": search})
    return s.text.strip() if s is not None else ""


def get_value_for_string(obj, strg):
    value = str(getattr(obj, strg, '')).replace("'", "''")
    value = "'" + value + "'"
#    logger.debug(f'get_value_for_string: {value}')
    return value

def get_values_for_strings(obj, strgs):
    my_str = ', '.join([get_value_for_string(obj, val) for val in strgs])
#    logger.debug(f'get_values_for_strings: {my_str}')
    return my_str

def get_value_for_number(obj, strg):
    value = getattr(obj, strg, 0)
#    logger.debug(f'get_value_for_number({obj}, {strg}: {value}')
    nmbr = value if strg == 'leg' else make_pp_pool_nmbr(value)
#    logger.debug(f'make_pp_pool_nmbr({value}: {nmbr}')
#    logger.debug(f'get_value_for_number: {str(nmbr)}')
    return str(nmbr)

def get_values_for_numbers(obj, nmbrs):
    my_str = ', '.join([get_value_for_number(obj, val) for val in nmbrs])
#    logger.debug(f'get_values_for_numbers: {my_str}')
    return my_str

def get_value_for_bool(obj, strg):
    value = getattr(obj, strg, False)
#    logger.debug(f'get_value_for_bool: {value}')
    return "1" if value else "0"

def get_values_for_bools(obj, bools):
    my_str = ', '.join([get_value_for_bool(obj, val) for val in bools])
#    logger.debug(f'get_values_for_bools: {my_str}')
    return my_str

pp_strip = re.compile("[-A-Za-z£,%() ]")

def make_pp_pool_nmbr(pp_units):
    """
    race - pp_pool: "£33,014.24 - Won"
    nag - pp_pool: "39.3"
    nag - pp_pool: 0
    nag - pp_pool: "Not backed"
    nag - pp_pool_perc: "(1%)"
    nag - pp_pool_perc: ""
    nag - pp_pool_perc: 0
    """
    stripped = pp_strip.sub("", str(pp_units))
    try:
        result = float(stripped)
    except Exception:
        result = 0
    logger.debug(f"make_pp_pool_nmbr({pp_units}) converted to {result}")
    return result


class Meeting:
    def __init__(self):
        self.name = ""
        self.race_date = ""
        self.start = ""
        self.type = ""
        self.going = ""
        self.stalls = ""
        self.pp_pool = 0
        self.pp_div = 0
        self.races = []

    def serialise_mtg(self):
        mtg = copy.copy(self)
        mtg.races = {}
        for card in self.races:
            mtg.races[card.name] = card.serialise_card()
        return mtg.__dict__

    def writemtg(self):
        if not os.path.isdir("./" + meetings_dir):
            os.mkdir("./" + meetings_dir)
        mtgkey = self.race_date + "-" + self.name
        pathname = meetings_dir + "/" + mtgkey
        with open(pathname + ".pickle", "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        ser = self.serialise_mtg()
        my_dict = {mtgkey: ser}
        with open(pathname + ".json", "w") as output:
            json.dump(my_dict, output)

    def write_summary_to_csv(self):
        if not os.path.isdir("./" + meetings_dir):
            os.mkdir("./" + meetings_dir)
        mtgkey = self.race_date + "-" + self.name
        pathname = meetings_dir + "/" + mtgkey
        with open(pathname + ".csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([f"Meeting: {self.name} date: {self.race_date}"])
            for race in self.races:
                writer.writerow([f"Race leg {race.leg} - {race.race_time} - {race.name} - Starters: {race.starters}"])
                writer.writerow(["Name", "N/R", "Result", "PP placed", "Placed", "PP pool", "PP pool perc", "Perc", "RP Forecast", "RP Win chance", "RP Place chance", "RP PP value", "SP", "SP Win chance", "SP Place chance", "SP PP value"])
                for nag in race.nags.values():
                    writer.writerow([nag.name, nag.nr, nag.result, nag.pp_placed, nag.placed, nag.pp_pool, nag.pp_pool_perc, nag.pp_pool_perc_calc,
                                     f"({nag.rp_forecast})", nag.rp_forecast_win_chance, nag.rp_forecast_place_chance, nag.rp_pp_value,
                                     f"({nag.sp})", nag.sp_win_chance, nag.sp_place_chance, nag.sp_pp_value])

    def write_mtg_to_db(self, db_name):
        connection = db.create_connection(db_name)
        db.execute_query(connection, self.insert_sql())
        db_mtg_key = db.execute_read_query(connection, self.retrieve_key_sql(), all=False)[0]
        if db_mtg_key is not None:
            for race in self.races:
                race.write_race_to_db(connection, db_mtg_key)

    def insert_sql(self):
        strings = ["name", "race_date", "start", "type", "going", "stalls"]
        numbers = ["pp_pool", "pp_div"]
        strg_vals = get_values_for_strings(self, strings)
        nmbr_vals = get_values_for_numbers(self, numbers)
        values = ', '.join([strg_vals, nmbr_vals])
        sql = f"INSERT INTO meeting ({', '.join(strings)}, {', '.join(numbers)}) VALUES ({values});"
        return sql

    def retrieve_key_sql(self):
        sql = f"SELECT id FROM meeting WHERE name = '{self.name}' AND race_date = '{self.race_date}'"
        return sql

    def collect_results(self, collect_pp, results):
        if collect_pp:
            logger.info(f"Collecting Tote pp for {self.name}")
            self.collect_ppresult()
        if results:
            logger.info(f"Collecting RP results for {self.name}")
            self.collect_rpresult()

    def collect_ppresult(self):
        urls = {}
        for race in self.races:
            if race.leg <= 6:
                urls[race.totepp_url] = race.leg
        results = tote.getpage_for_races(urls)
        for result in results:
            for card in self.races:
                if card.leg == result.leg:
                    card.set_toteresult(result)
                if card.leg == 1:
                    self.pp_pool = card.pp_pool

    def collect_rpresult(self):
        # collect the results from rp if they are there
        for race in self.races:
            race.collect_rpresult()

    def set_ppvalue(self):
        for race in self.races:
            race.set_rp_ppvalue()
            race.set_sp_ppvalue()


class Racecard:
    def __init__(self):
        self.mtgname = ""
        self.name = ""
        self.rp_id = ""
        self.rp_url = ""
        self.race_time = ""
        self.race_class = ""
        self.distance = ""
        self.field = ""
        self.verdict = ""
        self.pp_fav = 0
        self.pp_fav_perc = ""
        self.pp_nr = 0
        self.pp_pool = 0
        self.nags = {}
        self.totepp_url = ""
        self.leg = 0
        self.starters = 0
        self.rp_forecast_places = 0
        self.sp_places = 0

    def serialise_card(self):
        card = copy.copy(self)
        card.nags = {}
        for key, nag in self.nags.items():
            card.nags[key] = nag.__dict__
        return card.__dict__

    def write_race_to_db(self, connection, db_mtg_key):
        db.execute_query(connection, self.insert_sql(db_mtg_key))
        db_race_key = db.execute_read_query(connection, self.retrieve_key_sql(db_mtg_key), all=False)[0]
        if db_race_key is not None:
            for nag in self.nags.values():
                nag.write_nag_to_db(connection, db_race_key)

    def insert_sql(self, db_mtg_key):
        strings = ["name", "race_time", "race_class", "distance", "field", "verdict"]
        numbers = ["pp_pool", "pp_fav", "pp_fav_perc", "pp_nr", "leg", "starters"]
        strg_vals = get_values_for_strings(self, strings)
        nmbr_vals = get_values_for_numbers(self, numbers)
        values = ', '.join([strg_vals, nmbr_vals, f"{db_mtg_key}"])
        sql = f"INSERT INTO race ({', '.join(strings)}, {', '.join(numbers)}, meeting_id) VALUES ({values});"
        return sql

    def retrieve_key_sql(self, db_mtg_key):
        sql = f"""SELECT id FROM race WHERE leg = {self.leg} AND meeting_id = {db_mtg_key}"""
        return sql

    def find_nag(self, tote_nag):
        return self.find_nag_by_name(tote_nag.name.lower()) if not None \
            else self.find_nag_by_bib_or_draw(tote_nag)

    def find_nag_by_name(self, nagname):
        return self.nags.get(nagname.lower(), None)

    def find_nag_by_bib_or_draw(self, tote_nag):
        for nag in self.nags.values():
            if nag.no == tote_nag.bib:
                return nag
            if nag.draw != "" and nag.draw == f"({tote_nag.draw})":
                return nag
        return None

    def extract_rp_racecard(self, raw_card):
        try:
            self.name = raw_card.find("span", {"class": "RC-meetingItem__info"}).text.strip()
            self.rp_id = raw_card.find("a", {"class": "RC-meetingItem__link"})["data-race-id"]
            self.rp_url = raw_card.find("a", {"class": "RC-meetingItem__link"})["href"]
            self.race_time = raw_card.find("span", {"class": "RC-meetingItem__timeLabel"}).text.strip()
            my_words = raw_card.find("span", {"class": "RC-meetingItem__goingData"}).text.split()
            self.race_class = " ".join(my_words[0:-1])
            self.distance = my_words[-1]
            self.field = raw_card.find("span", {"class": "RC-meetingItem__numberOfRunners"}).text.strip()
        except: None
        self.set_tote_url()
        self.extract_rp_runners()

    def extract_rp_runners(self):
        fn_time = "_".join(self.race_time.split(":"))
        logger.info(f"Collecting {self.mtgname} - {self.race_time}", )
        fn_name = self.mtgname + "_" + fn_time
        # Verdict page
        verdictpage = getpage("https://www.racingpost.com/racecards/data/accordion/" + self.rp_id, fn_name + "_verdict")
        verdict_bs = BeautifulSoup(verdictpage, "html.parser")
        self.verdict = verdict_bs.find("div", {"class": "RC-raceVerdict__content"}).text.strip()
        # Extract runners
        runnerspage = getpage("https://www.racingpost.com" + self.rp_url, fn_name)
        runners_bs = BeautifulSoup(runnerspage, "html.parser")
        raw_nags = runners_bs.findAll("div", {"class": "RC-runnerRow"})
        for raw_nag in raw_nags:
            nag = Nag()
            nag.extract_rp_nag(raw_nag)
            self.nags[nag.name.lower()] = nag if nag.name else None
        # Extract betting forecast
        forecast_groups = runners_bs.findAll("span", {"data-test-selector": "RC-bettingForecast_group"})
        for group in forecast_groups:
            self.extract_rp_forecast(group)
        self.set_rp_forecast_chance()

    def extract_rp_forecast(self, group):
        odds = group.text.split()[0]
        nags = group.findAll("a")
        for nagname in nags:
            nag = self.find_nag_by_name(nagname.text)
            nag.rp_forecast = odds if nag is not None else None

    def set_tote_url(self):
        racetime = self.race_time.split(":")
        hours = int(racetime[0])
        if  hours < 10:
            racetime[0] = str(hours + 12)
        tote_coursename = courselist_dict[self.mtgname]
        self.totepp_url = f"https://tote.co.uk/results/{tote_coursename}/{racetime[0]}:{racetime[1]}/placepot"

    def set_toteresult(self, result):
        # extract the details of result into card
        self.pp_pool = make_pp_pool_nmbr(result.pool)
        self.pp_fav = make_pp_pool_nmbr(result.fav_pp)
        self.pp_fav_perc = make_pp_pool_nmbr(result.fav_pp_perc)
        # run through the nags and find mapping nag, then extract results back into here
        for pp_nag in result.pp_nags:
            nag = self.find_nag(pp_nag)
            if nag is not None:
                #   map the individual fields
                nag.placed = pp_nag.placed
                nag.pp_placed = pp_nag.placed
                nag.pp_pool = make_pp_pool_nmbr(pp_nag.pp_units)
                nag.pp_pool_perc = make_pp_pool_nmbr(pp_nag.pp_percent)

    def collect_rpresult(self):
        # collect the results from the racingpost page
        fn_time = "_".join(self.race_time.split(":"))
        fn_name = f"{self.mtgname}_{fn_time}"
        logger.info(f"Collecting results for {fn_name}")
        resultsurl = "https://www.racingpost.com" + self.rp_url.replace("racecards", "results")
        resultspage = getpage(resultsurl, fn_name + "_result")
        runners_bs = BeautifulSoup(resultspage, "html.parser")
#        raw_nags = runners_bs.findAll("tr", {"class": "rp-horse_Table__mainRow"})
        raw_nags = runners_bs.findAll("tr")
        self.starters = 0
        for raw_nag in raw_nags:
            nagname = find_or_empty(raw_nag, "a", "rp-horseTable__horse__name")
            nagresult = find_or_empty(raw_nag, "span", "rp-horseTable__pos__number")
            nag_sp = find_or_empty(raw_nag, "span", "rp-horseTable__horse__price")
            nag = self.nags.get(nagname.lower())
            if nag:
                nag.sp = nag_sp
                nag.result = nagresult
                self.starters += 1
        self.set_starters_and_nr_flag()
        self.set_sp_chance()

    def set_starters_and_nr_flag(self):
        non_runners = 0
        for nag in self.nags.values():
            if not nag.sp:
                nag.nr = True
                non_runners += 1
            else:
                nag.nr = False
        self.starters = len(self.nags) - non_runners

    def set_places_for(self, field_size):
        if field_size < 5:
            return 1
        elif field_size < 8:
            return 2
        elif field_size < 16:
            return 3
        elif self.is_handicap():
            return 4
        elif self.is_nursery():
            return 4
        else:
            return 3

    def is_handicap(self):
        return "handicap" in self.name.lower()

    def is_nursery(self):
        return "nursery" in self.name.lower()

    def set_rp_forecast_places(self):
        self.rp_forecast_places = self.set_places_for(len(self.nags))

    def set_sp_places(self):
        if not self.starters:
            self.set_starters_and_nr_flag()
        self.sp_places = self.set_places_for(self.starters)


    def set_rp_forecast_chance(self):
        rp_forecast_odds = [nag.rp_forecast for nag in self.nags.values()]
        if not getattr(self, "rp_forecast_places", False):
            self.set_rp_forecast_places()
        chance_dict = odds.get_place_chances_for(rp_forecast_odds, self.rp_forecast_places)
        for nag in self.nags.values():
            chance = chance_dict.get(nag.rp_forecast, [0, 0])
            nag.rp_forecast_win_chance = chance[0]
            nag.rp_forecast_place_chance = chance[1]

    def set_sp_chance(self):
        sp_odds = [nag.sp for nag in self.nags.values()]
        if not getattr(self, "sp_places", False):
            self.set_sp_places()
        chance_dict = odds.get_place_chances_for(sp_odds, self.sp_places)
        for nag in self.nags.values():
            chance = chance_dict.get(nag.sp, [0, 0])
            nag.sp_win_chance = chance[0]
            nag.sp_place_chance = chance[1]
            nag.set_placed(self.sp_places)

    def set_rp_ppvalue(self):
        rp_val = {}
        for nag in self.nags.values():
            try:
                pool = float(nag.pp_pool)
            except:
                pool = 0
            if nag.rp_forecast_win_chance > 0:
                rp_val[nag.name] = [pool, nag.rp_forecast_win_chance, nag.rp_forecast_place_chance, nag.sp_win_chance]
        rp_val_dict = pp_value.calc_pp_value(rp_val, self.rp_forecast_places)
        for nag in self.nags.values():
            try:
                nag.pp_pool_perc_calc = rp_val_dict[nag.name][0]
                nag.rp_pp_value = rp_val_dict[nag.name][1]
            except:
                nag.pp_pool_perc_calc = 0
                nag.rp_pp_value = 0

    def set_sp_ppvalue(self):
        sp_val = {}
        for nag in self.nags.values():
            try:
                pool = float(nag.pp_pool)
            except:
                pool = 0
            if nag.sp_win_chance > 0:
                sp_val[nag.name] = [pool, nag.sp_win_chance, nag.sp_place_chance, nag.sp_win_chance]
        sp_val_dict = pp_value.calc_pp_value(sp_val, self.sp_places)
        for nag in self.nags.values():
            try:
                nag.pp_pool_perc_calc = sp_val_dict[nag.name][0]
                nag.sp_pp_value = sp_val_dict[nag.name][1]
            except:
                nag.pp_pool_perc_calc = 0
                nag.sp_pp_value = 0


class Nag:
    def __init__(self):
        self.name = ""
        self.rp_id = ""
        self.no = ""
        self.draw = ""
        self.lastrun = ""
        self.form = ""
        self.age = ""
        self.jockey = ""
        self.trainer = ""
        self.ts = ""
        self.rpr = ""
        self.rp_comment = ""
        self.rp_forecast = ""
        self.bet365_odds = []
        self.best_odds = []
        self.bf_odds = []
        self.result = ""
        self.sp = ""
        self.fav = ""
        self.race_comment = ""
        self.pp_pool = 0
        self.pp_pool_perc = 0
        self.pp_placed = False
        self.placed = False
        self.rp_forecast_win_chance = 0
        self.rp_forecast_place_chance = 0
        self.sp_win_chance = 0
        self.sp_place_chance = 0
        self.nr = False
        self.rp_pp_value = 0
        self.sp_pp_value = 0
        self.pp_pool_perc_calc = 0

    def write_nag_to_db(self, connection, db_race_key):
        db.execute_query(connection, self.insert_sql(db_race_key))

    def insert_sql(self, db_race_key):
        strings = ["name", "no", "draw", "lastrun", "form", "age", "jockey", "trainer", "ts", "rpr",
                   "rp_comment", "rp_forecast", "result", "sp", "fav", "race_comment", "pp_pool_perc"]
        bools = ["pp_placed", "placed", "nr"]
        numbers = ["pp_pool", "pp_pool_perc_calc", "rp_forecast_win_chance", "rp_forecast_place_chance",
                   "rp_pp_value", "sp_win_chance", "sp_place_chance", "sp_pp_value"]
        strg_vals = get_values_for_strings(self, strings)
        bool_vals = get_values_for_bools(self, bools)
        nmbr_vals = get_values_for_numbers(self, numbers)
        values = ', '.join([strg_vals, bool_vals, nmbr_vals, f"{db_race_key}"])
        sql = f"INSERT INTO nag ({', '.join(strings)}, {', '.join(bools)}, {', '.join(numbers)}, race_id) VALUES ({values});"
        return sql

    def extract_rp_nag(self, raw_nag):
        self.rp_id = raw_nag["data-ugc-runnerid"]
        self.name = find_or_empty(raw_nag, "a", "RC-runnerName")
        self.no = find_or_empty(raw_nag, "span", "RC-runnerNumber__no")
        self.draw = find_or_empty(raw_nag, "span", "RC-runnerNumber__draw")
        self.lastrun = find_or_empty(raw_nag, "div", "RC-runnerStats__lastRun")
        self.form = find_or_empty(raw_nag, "span", "RC-runnerInfo__form")
        self.age = find_or_empty(raw_nag, "span", "RC-runnerAge")
        jockey_outer = raw_nag.find("div", {"class": "RC-runnerInfo_jockey"})
        self.jockey = find_or_empty(jockey_outer, "a", "RC-runnerInfo__name")
        trainer_outer = raw_nag.find("div", {"class": "RC-runnerInfo_trainer"})
        self.trainer = find_or_empty(trainer_outer, "a", "RC-runnerInfo__name")
        self.ts = find_or_empty(raw_nag, "span", "RC-runnerTs")
        self.rpr = find_or_empty(raw_nag, "span", "RC-runnerRpr")
        self.rp_comment = find_or_empty(raw_nag, "div", "RC-comments__content")

    def set_placed(self, places):
        try:
            place = int(self.result.split()[0])
        except:
            place = 99
        self.placed = (place <= places)


def extract_rp_meeting(raw_mtg, sel_mtg):
    name = raw_mtg.find("span", {"class": "RC-accordion__courseName"}).text.split()[0].lower()
    if sel_mtg and name != sel_mtg:
        return None
    racecount_bs = raw_mtg.find("span", {"class": "RC-accordion__raceCount"})
    if racecount_bs is None:
        return None
    try:
        racecount_str = racecount_bs.text.split()[0]
        racecount = int(racecount_str)
    except:
        return None
    if racecount < 6 or \
            name not in courselist_dict.keys() or \
            raw_mtg.find("span", {"class": "RC-accordion__abandonedLabel"}) is not None:
        return None
    mtg = Meeting()
    mtg.name = name
    logger.info(f"Collecting {name}")
    mtg.race_date = date.today().strftime('%Y-%m-%d')
    #TODO - get proper date
    mtg.start = raw_mtg.find("span", {"data-test-selector": "RC-accordion__firstRaceTime"}).text.strip()
    mtg.type = raw_mtg.find("span", {"class": "RC-accordion__meetingType"}).text.strip()
    mtg.going = raw_mtg.find("div", {"class": "RC-courseDescription__info"}).text.strip()
    raw_racecards = raw_mtg.findAll("div", {"class": "RC-meetingItem"})
    #TODO - here we need to catch half abandoned races
    leg = 0
    for raw_racecard in raw_racecards:
        leg += 1
        card = Racecard()
        card.mtgname = name
        card.leg = leg
        card.extract_rp_racecard(raw_racecard)
        if card is not None: mtg.races.append(card)
    return mtg


# my_mtg = unpickle_mtg("mtg\\2020-10-17-ascot.picle")

