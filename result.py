from dataclasses import dataclass
from datetime import date


@dataclass
class Result:
    pos: str = ''
    bib: str = ''
    name: str = ''
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
    t1: str = ''
    bike: str = ''
    t2: str = ''
    run: str = ''
    time: str = ''
    winningtime: str = ''

@dataclass
class Race():
    date: str = ''
    event: str = ''
    url: str = ''
    location: str = ''
    distance: str = ''
    type: str = ''
    winningtime: str = ''
