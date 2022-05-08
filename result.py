from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class Participant:
    pos: str = ''
    bib: str = ''
    name: str = ''
    firstname: str = ''
    surname: str = ''
    club: str = ''
    gender: str = ''
    age: str = ''
    category: str = ''
    date: str = ''
    race: str = ''
    racetype: str = ''
    location: str = ''
    distance: str = ''  # 5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
    comment: str = ''
    swim: str = ''
    run1: str = ''
    t1: str = ''
    bike: str = ''
    t2: str = ''
    run2: str = ''
    run: str = ''
    time: str = ''
    winningtime: str = ''

    @staticmethod
    def fields():
        return Participant.__dict__.keys()

    def to_dict(self):
        return asdict(self)

    def duathlon(self):
        return True if self.run1 and self.bike else False

    def triathlon(self):
        return True if self.swim and self.bike else False

    def textoutput(self):
        if self.duathlon():
            return f"pos: {self.pos} name: {self.name} cat: {self.category} run1: {self.run1} t1: {t1} bike: {self.bike} t2: {self.t2} run2: {self.run2} total: {self.time}"
        elif self.triathlon():
            return f"pos: {self.pos} name: {self.name} cat: {self.category} swim: {self.swim} t1: {t1} bike: {self.bike} t2: {self.t2} run: {self.run} total: {self.time}"
        else:
            return f"pos: {self.pos} name: {self.name} cat: {self.category} time: {self.time}"

    def tableoutput(self):
        if self.duathlon():
            return f"<tr><td>{self.pos}</td><td>{self.name}</td><td>{self.category}</td><td>{self.run1}</td><td>{t1}</td><td>{self.bike}</td><td>{self.t2}</td><td>{self.run2}</td><td>{self.time}</td></tr>"
        elif self.triathlon():
            return f"<tr><td>{self.pos}</td><td>{self.name}</td><td>{self.category}</td><td>{self.swim}</td><td>{t1}</td><td>{self.bike}</td><td>{self.t2}</td><td>{self.run}</td><td>{self.time}</td></tr>"
        else:
            return f"<tr><td>{self.pos}</td><td>{self.name}</td><td>{self.category}</td><td>{self.time}</td></tr>"


@dataclass
class Race():
    date: str = ''
    event: str = ''
    url: str = ''
    location: str = ''
    distance: str = ''
    type: str = ''
    winningtime: str = ''
    year: str = ''
    base_url: str = ''
    participants: List = field(default_factory=lambda: [Participant])

    def duathlon(self):
        return True if self.participants and self.participants[0].duathlon() else False

    def triathlon(self):
        return True if self.participants and self.participants[0].triathlon() else False

    def tableheaderoutput(self):
        tabledef = '<div class="table-1"><table width="100%"><thead>'
        tabledefend = '</thead><tbody>'
        if self.duathlon():
            return f"{tabledef}<tr><th>pos</th><th>name</th><th>cat</th><th>run1</th><th>t1</th><th>bike</th><th>t2</th><th>run2</th><th>total</th></th>{tabledefend}"
        elif self.triathlon():
            return f"{tabledef}<tr><th>pos</th><th>name</th><th>cat</th><th>swim</th><th>t1</th><th>bike</th><th>t2</th><th>run</th><th>total</th></th>{tabledefend}"
        else:
            return f"{tabledef}<tr><th>pos</th><th>name</th><th>cat</th><th>time</th></tr>{tabledefend}"

    def tableend(self):
        return '</tbody></table></div>'

    def html_race_output(self):
        output = ""
        if self.participants:
            output = f"<h3><b>{self.date} - {self.event}</b></h3>{self.tableheaderoutput()}"
            for runner in self.participants:
                output += runner.tableoutput()
            output += self.tableend()
        return output

