# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
import os

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
        self.name = ""
        self.rp_id = ""
        self.rp_url = ""
        self.race_time = ""
        self.race_class = ""
        self.distance = ""
        self.field = ""
        self.verdict = ""
        self.pp_fav = 0
        self.pp_nr = 0
        self.pp_pool = 0
        self.nags = []

class Nag:
    def __init__(self):
        self.name = ""
        self.no = 0
        self.draw = 0
        self.form = ""
        self.age = 0
        self.weight = ""
        self.rp_or = 0
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


def getpage(url, name):
    html = urlopen(url)
    if not os.path.isdir("./pages"):
        os.mkdir("./pages")
    today = date.today().strftime('%Y-%m-%d')
    if not os.path.isdir("./pages/"+today):
        os.mkdir("./pages/"+today)
    pathname = "pages/" + today + "/" + name + ".html"
    output = open(pathname, "wb")
    output.writelines(html.readlines())
    output.close()
    return open(pathname).read()

def extract_rp_racecard(raw_card):
    card = Racecard()
    card.name = raw_card.find("span", {"class":"RC-meetingItem__info"}).text.strip()
    card.rp_id = raw_card.find("a", {"class":"RC-meetingItem__link"})["data-race-id"]
    card.rp_url = raw_card.find("a", {"class":"RC-meetingItem__link"})["href"]
    card.race_time = raw_card.find("span", {"class":"RC-meetingItem__timeLabel"}).text.strip()
    words = raw_card.find("span", {"class":"RC-meetingItem__goingData"}).text.split()
    card.race_class = " ".join(words[0:-1])
    card.distance = words[-1]
    card.field = raw_card.find("span", {"class":"RC-meetingItem__numberOfRunners"}).text.strip()
    card.verdict = ""
    return card


def extract_rp_meeting(raw_mtg):
    mtg = Meeting()
    mtg.name = raw_mtg.find("span", {"class":"RC-accordion__courseName"}).text.strip()
# list of meetings that I want to process
    mtg.date = str(date.today())
    mtg.start = raw_mtg.find("span", {"data-test-selector":"RC-accordion__firstRaceTime"}).text.strip()
    mtg.type = raw_mtg.find("span", {"class":"RC-accordion__meetingType"}).text.strip()
    mtg.going = raw_mtg.find("div", {"class":"RC-courseDescription__info"}).text.strip()
    raw_racecards = raw_mtg.findAll("div", {"class":"RC-meetingItem"})
    for raw_racecard in raw_racecards:
        racecard = extract_rp_racecard(raw_racecard)
        mtg.races.append(racecard)
    return mtg

def read_racingpost_index():
    bs = BeautifulSoup(getpage("https://www.racingpost.com/racecards/", "rpindex"), "html.parser")
    raw_meetings = bs.findAll("section", {"class":"ui-accordion__row"})
    meetings = []
    for raw_mtg in raw_meetings:
        mtg = extract_rp_meeting(raw_mtg)
        meetings.append(mtg)
# save meetings


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_racingpost_index()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
