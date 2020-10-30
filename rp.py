from bs4 import BeautifulSoup
from datetime import date
from fractions import Fraction
import os
import requests
import json
import pickle
import tote
import copy

demo_odds = Fraction("5/2")


infile = open('courselist_tote.txt')
courselist_dict = {}
for line in infile.read().split("\n"):
    words = line.split()
    if len(words) > 1:
        courselist_dict[words[0].strip().lower()] = words[1].strip().lower()
    else:
        courselist_dict[words[0].strip().lower()] = words[0].strip().lower()


def read_racingpost_index(sel_mtg, collect_pp, results):
    bs = BeautifulSoup(getpage("https://www.racingpost.com/racecards/", "rpindex"), "html.parser")
    raw_meetings = bs.findAll("section", {"class": "ui-accordion__row"})
    for raw_mtg in raw_meetings:
        mtg = extract_rp_meeting(raw_mtg, sel_mtg)
        if mtg is not None:
            mtg.collect_results(collect_pp, results)
            print(f"Saving {mtg.name}")
            mtg.writemtg()


def load_meeting_and_collect_results(filename, collect_pp, results):
    with open(filename, "rb") as mtgfile:
        mtg = None
        try:
            mtg = pickle.load(mtgfile)
        except Exception:
            print(f"Can't unpickle {filename}")
        if isinstance(mtg, Meeting):
            print("We have a meeting")
            mtg.collect_results(collect_pp, results)
            print(f"Saving {mtg.name}")
            mtg.writemtg()


def getpage(url, name):
    r = requests.get(url)
    if r.status_code > 299:
        print(f"No results available for {name}")
        return ""
    html = r.text
    return html


def find_or_empty(bs, key, search):
    if bs is None:
        return ""
    s = bs.find(key, {"class": search})
    return s.text.strip() if s is not None else ""


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
        if not os.path.isdir("./meetings"):
            os.mkdir("./meetings")
        mtgkey = self.race_date + "-" + self.name
        pathname = "meetings/" + mtgkey
        with open(pathname + ".pickle", "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        ser = self.serialise_mtg()
        my_dict = {mtgkey: ser}
        with open(pathname + ".json", "w") as output:
            json.dump(my_dict, output)

    def collect_results(self, collect_pp, results):
        if collect_pp:
            print(f"Collecting Tote pp for {self.name}")
            self.collect_ppresult()
        if results:
            print(f"Collecting RP results for {self.name}")
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

    def collect_rpresult(self):
        # collect the results from rp if they are there
        for race in self.races:
            race.collect_rpresult()


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

    def serialise_card(self):
        card = copy.copy(self)
        card.nags = {}
        for key, nag in self.nags.items():
            card.nags[key] = nag.__dict__
        return card.__dict__

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
        self.name = raw_card.find("span", {"class": "RC-meetingItem__info"}).text.strip()
        self.rp_id = raw_card.find("a", {"class": "RC-meetingItem__link"})["data-race-id"]
        self.rp_url = raw_card.find("a", {"class": "RC-meetingItem__link"})["href"]
        self.race_time = raw_card.find("span", {"class": "RC-meetingItem__timeLabel"}).text.strip()
        my_words = raw_card.find("span", {"class": "RC-meetingItem__goingData"}).text.split()
        self.race_class = " ".join(my_words[0:-1])
        self.distance = my_words[-1]
        self.field = raw_card.find("span", {"class": "RC-meetingItem__numberOfRunners"}).text.strip()
        self.set_tote_url()
        self.extract_rp_runners()

    def extract_rp_runners(self):
        fn_time = "_".join(self.race_time.split(":"))
        print(f"Collecting {self.mtgname} - {self.race_time}", )
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
        self.pp_pool = result.pool
        self.pp_fav = result.fav_pp
        self.pp_fav_perc = result.fav_pp_perc
        # run through the nags and find mapping nag, then extract results back into here
        for pp_nag in result.pp_nags:
            nag = self.find_nag(pp_nag)
            if nag is not None:
                #   map the individual fields
                nag.placed = pp_nag.placed
                nag.pp_pool = pp_nag.pp_units
                nag.pp_pool_perc = pp_nag.pp_percent

    def collect_rpresult(self):
        # collect the results from the racingpost page
        fn_time = "_".join(self.race_time.split(":"))
        fn_name = f"{self.mtgname}_{fn_time}"
        print(f"Collecting results for {fn_name}")
        resultsurl = "https://www.racingpost.com" + self.rp_url.replace("racecards", "results")
        resultspage = getpage(resultsurl, fn_name + "_result")
        runners_bs = BeautifulSoup(resultspage, "html.parser")
#        raw_nags = runners_bs.findAll("tr", {"class": "rp-horse_Table__mainRow"})
        raw_nags = runners_bs.findAll("tr")
        for raw_nag in raw_nags:
            nagname = find_or_empty(raw_nag, "a", "rp-horseTable__horse__name")
            nagresult = find_or_empty(raw_nag, "span", "rp-horseTable__pos__number")
            nag_sp = find_or_empty(raw_nag, "span", "rp-horseTable__horse__price")
            nag = self.nags.get(nagname.lower())
            if nag:
                nag.sp = nag_sp
                nag.result = nagresult


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
        self.rp_forecast = 0
        self.bet365_odds = []
        self.best_odds = []
        self.bf_odds = []
        self.result = ""
        self.sp = 0
        self.fav = ""
        self.race_comment = ""
        self.pp_pool = 0
        self.pp_pool_perc = ""
        self.placed = False

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
    print(f"Collecting {name}")
    mtg.race_date = date.today().strftime('%Y-%m-%d')
    mtg.start = raw_mtg.find("span", {"data-test-selector": "RC-accordion__firstRaceTime"}).text.strip()
    mtg.type = raw_mtg.find("span", {"class": "RC-accordion__meetingType"}).text.strip()
    mtg.going = raw_mtg.find("div", {"class": "RC-courseDescription__info"}).text.strip()
    raw_racecards = raw_mtg.findAll("div", {"class": "RC-meetingItem"})
    leg = 0
    for raw_racecard in raw_racecards:
        leg += 1
        card = Racecard()
        card.mtgname = name
        card.leg = leg
        card.extract_rp_racecard(raw_racecard)
        mtg.races.append(card)
    return mtg
