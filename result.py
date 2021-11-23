from datetime import date, timedelta


class Result:
    def __init__(self):
        self.pos = ''
        self.bib = ''
        self.runner = ''
        self.club = ''
        self.gender = ''
        self.age = 0
        self.category = ''
        self.date =
        self.race = ''
        self.distance = ''       #5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
        self.swimtime = 0
        self.swimtransition = 0
        self.biketime = 0
        self.biketransition = 0
        self.runtime = 0
        self.comment = ''


class Race():
    def __init__(self):
        self.date = ''
        self.event = ''
        self.url = ''
        self.location = ''
        self.distance = ''
        self.type = ''
