from datetime import date, timedelta


class Result:
    def __init__(self):
        self.runner = ''
        self.gender = ''
        self.age = 0
        self.category = ''
        self.date = date.today()
        self.race = ''
        self.distance = ''       #5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
        self.swimtime = timedelta(seconds=0)
        self.swimtransition = timedelta(seconds=0)
        self.biketime = timedelta(seconds=0)
        self.biketransition = timedelta(seconds=0)
        self.runtime = timedelta(seconds=0)
        self.comment = ''


class Race():
    def __init__(self):
        self.date = date.today()
        self.event = ''
        self.url = ''
        self.location = ''
        self.distance = ''
        self.type = ''
