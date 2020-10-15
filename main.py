from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from fractions import Fraction
import os
import requests
import json
import pickle
import tote

demo_odds = Fraction("5/2")

infile = open('courselist_tote.txt')
global courselist_dict
courselist_dict = {}
for line in infile.read().split("\n"):
    words = line.split()
    if len(words) > 1:
        courselist_dict[words[0].strip().lower()] = words[1].strip().lower()
    else:
        courselist_dict[words[0].strip().lower()] = words[0].strip().lower()

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
        self.nags = []
        self.totepp_url = ""
        self.leg = 0

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

def writepage(text, name):
    if not os.path.isdir("./pages"):
        os.mkdir("./pages")
    today = date.today().strftime('%Y-%m-%d')
    if not os.path.isdir("./pages/"+today):
        os.mkdir("./pages/"+today)
    pathname = "pages/" + today + "/" + name + ".html"
    with open(pathname, "w") as output:
        output.write(text)

def writemtg(mtg):
    if not os.path.isdir("./meetings"):
        os.mkdir("./meetings")
    today = date.today().strftime('%Y-%m-%d')
    mtgkey = today + "-" + mtg.name
    pathname = "meetings/" + mtgkey
    with open(pathname + ".picle", "wb") as f:
        pickle.dump(mtg, f, pickle.HIGHEST_PROTOCOL)
    ser = mtg.__dict__
    cards = []
    for card in mtg.races:
        nags = []
        for nag in card.nags:
            nags.append(nag.__dict__)
        carddict = card.__dict__
        carddict["nags"] = nags
        cards.append(carddict)
    ser["races"] = cards
    dict = {mtgkey : ser}
    with open(pathname + ".json", "w") as output:
        json.dump(dict, output)

def getpage(url, name):
    r = requests.get(url)
    if r.raise_for_status() != None:
        print(f"Error getting {url} - {name}")
        return ""
    html = r.text
    writepage(html, name)
    return html

def find_or_empty(bs, key, search):
    if bs == None:
        return ""
    s = bs.find(key, {"class":search})
    return s.text.strip() if s != None else ""


def build_tote_url(race):
    racetime = race.race_time.split(":")
    if int(racetime[0]) < 12:
        racetime[0] = str(int(racetime[0]) + 12)
    tote_coursename = courselist_dict[race.mtgname]
    return f"https://tote.co.uk/results/{tote_coursename}/{racetime[0]}:{racetime[1]}/placepot"


def extract_rp_nag(raw_nag):
    nag = Nag()
    nag.rp_id = raw_nag["data-ugc-runnerid"]
    nag.name = find_or_empty(raw_nag, "a", "RC-runnerName")
    nag.no = find_or_empty(raw_nag, "span", "RC-runnerNumber__no")
    nag.draw = find_or_empty(raw_nag, "span", "RC-runnerNumber__draw")
    nag.lastrun = find_or_empty(raw_nag, "div", "RC-runnerStats__lastRun")
    nag.form = find_or_empty(raw_nag, "span", "RC-runnerInfo__form")
    nag.age = find_or_empty(raw_nag, "span", "RC-runnerAge")
    jockey_outer = raw_nag.find("div", {"class":"RC-runnerInfo_jockey"})
    nag.jockey = find_or_empty(jockey_outer, "a", "RC-runnerInfo__name")
    trainer_outer = raw_nag.find("div", {"class":"RC-runnerInfo_trainer"})
    nag.trainer = find_or_empty(trainer_outer, "a", "RC-runnerInfo__name")
    nag.ts = find_or_empty(raw_nag, "span", "RC-runnerTs")
    nag.rpr = find_or_empty(raw_nag, "span", "RC-runnerRpr")
    nag.rp_comment = find_or_empty(raw_nag, "div", "RC-comments__content")
    return nag


def extract_rp_runners(card):
    fn_time = "_".join(card.race_time.split(":"))
    fn_mtg = card.mtgname
    print(f"Collecting {fn_mtg} - {card.race_time}", )
    fn_name = fn_mtg + "_" + fn_time
    # Verdict page
    verdictpage = getpage("https://www.racingpost.com/racecards/data/accordion/" + card.rp_id, fn_name + "_verdict")
    verdict_bs = BeautifulSoup(verdictpage, "html.parser")
    card.verdict = verdict_bs.find("div", {"class":"RC-raceVerdict__content"}).text.strip()
    # Extract runners
    runnerspage = getpage("https://www.racingpost.com" + card.rp_url, fn_name)
    runners_bs = BeautifulSoup(runnerspage, "html.parser")
    raw_nags = runners_bs.findAll("div", {"class":"RC-runnerRow"})
    for raw_nag in raw_nags:
        nag = extract_rp_nag(raw_nag)
        card.nags.append(nag) if nag != None else None
    # Extract betting forecast
    forecast_groups = runners_bs.findAll("span", {"data-test-selector": "RC-bettingForecast_group"})
    for group in forecast_groups:
        extract_rp_forecast(group, card)

def extract_rp_forecast(group, card):
    odds = group.text.split()[0]
    nags = group.findAll("a")
    for nagname in nags:
        nag = find_nag_by_name(card, nagname.text)
        nag.rp_forecast = odds if nag is not None else None

def find_nag_by_name(card, nagname):
    for nag in card.nags:
        if nag.name.lower() == nagname.lower():
            return nag
    return None

def extract_rp_racecard(raw_card, mtg, leg):
    card = Racecard()
    card.mtgname = mtg.name
    card.leg = leg
    card.name = raw_card.find("span", {"class":"RC-meetingItem__info"}).text.strip()
    card.rp_id = raw_card.find("a", {"class":"RC-meetingItem__link"})["data-race-id"]
    card.rp_url = raw_card.find("a", {"class":"RC-meetingItem__link"})["href"]
    card.race_time = raw_card.find("span", {"class":"RC-meetingItem__timeLabel"}).text.strip()
    words = raw_card.find("span", {"class":"RC-meetingItem__goingData"}).text.split()
    card.race_class = " ".join(words[0:-1])
    card.distance = words[-1]
    card.field = raw_card.find("span", {"class":"RC-meetingItem__numberOfRunners"}).text.strip()
    card.totepp_url = build_tote_url(card)
    extract_rp_runners(card)
    return card

def find_nag(card, tote_nag):
    for nag in card.nags:
        if nag.no == tote_nag.bib:
            return nag
        if nag.draw != "" and nag.draw == f"({tote_nag.draw})":
            return nag
    return None

def get_toteresult(card):
    # check that the race has already been run
    result = tote.getpage_for_leg(card.totepp_url, card.leg)
    # extract the details of result into card
    card.pp_pool = result.pool
    card.pp_fav = result.fav_pp
    card.pp_fav_perc = result.fav_pp_perc
    # run through the nags and find mapping nag, then extract results back into here
    for pp_nag in result.pp_nags:
        nag = find_nag(card, pp_nag)
        if nag is not None:
        # map the individual fields
            nag.placed = pp_nag.placed
            nag.pp_pool = pp_nag.pp_units
            nag.pp_pool_perc = pp_nag.pp_percent
    return card

def extract_rp_meeting(raw_mtg):
    name = raw_mtg.find("span", {"class": "RC-accordion__courseName"}).text.split()[0].lower()
    racecount = 0
    racecount_bs = raw_mtg.find("span", {"class": "RC-accordion__raceCount"})
    if racecount_bs == None:
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
    mtg.race_date = str(date.today())
    mtg.start = raw_mtg.find("span", {"data-test-selector":"RC-accordion__firstRaceTime"}).text.strip()
    mtg.type = raw_mtg.find("span", {"class":"RC-accordion__meetingType"}).text.strip()
    mtg.going = raw_mtg.find("div", {"class":"RC-courseDescription__info"}).text.strip()
    raw_racecards = raw_mtg.findAll("div", {"class":"RC-meetingItem"})
    leg = 0
    for raw_racecard in raw_racecards:
        leg += 1
        racecard = extract_rp_racecard(raw_racecard, mtg, leg)
        get_toteresult(racecard) if leg <= 6 else None
        mtg.races.append(racecard)
    return mtg

def read_racingpost_index():
    bs = BeautifulSoup(getpage("https://www.racingpost.com/racecards/", "rpindex"), "html.parser")
    raw_meetings = bs.findAll("section", {"class":"ui-accordion__row"})
    meetings = []
    for raw_mtg in raw_meetings:
        mtg = extract_rp_meeting(raw_mtg)
        if mtg != None:
            writemtg(mtg)
            meetings.append(mtg)
# save meetings


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_racingpost_index()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
