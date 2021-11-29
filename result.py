from dataclasses import dataclass
from datetime import date


@dataclass
class Result:
    pos: str
    bib: str
    runner: str
    club: str
    gender: str
    age: int
    category: str
    date: date
    race: str
    distance: str  # 5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
    swimtime: int
    swimtransition: int
    biketime: int
    biketransition: int
    runtime: int
    comment: str

@dataclass
class Race():
    date: str
    event: str
    url: str
    location: str
    distance: str
    type: str
