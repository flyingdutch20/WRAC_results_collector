from dataclasses import dataclass
from datetime import date


@dataclass
class Result:
    pos: str = ''
    bib: str = ''
    runner: str = ''
    club: str = ''
    gender: str = ''
    age: int = 0
    category: str = ''
    date: date = date.today()
    race: str = ''
    distance: str = ''  # 5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
    comment: str = ''
    swimtime: int = None
    swimtransition: int = None
    biketime: int = None
    biketransition: int = None
    runtime: int = None

@dataclass
class Race():
    date: str = ''
    event: str = ''
    url: str = ''
    location: str = ''
    distance: str = ''
    type: str = ''
