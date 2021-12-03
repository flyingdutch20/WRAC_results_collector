import pytest
from datetime import date

import result

today = date.today()

class TestResult():
    def test_access_result(self):
        res = result.Result('1','123','Jopie','WRAC','M',25,'MSEN',today,'W10K','10k','',runtime=3600)
        assert res.pos == '1'
        assert res.bib == '123'
        assert res.runner == 'Jopie'
        assert res.club == 'WRAC'
        assert res.gender == 'M'
        assert res.age == 25
        assert res.category == 'MSEN'
        assert res.date == today
        assert res.race == 'W10K'
        assert res.distance == '10k'  # 5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
        assert res.comment == ''
        assert res.swimtime is None
        assert res.swimtransition is None
        assert res.biketime is None
        assert res.biketransition is None
        assert res.runtime == 3600


class TestRace():
    def test_access_race(self):
        race = result.Race('10-Sep-2021','Wetherby 10k','/1234','Wetherby','10k','road')
        assert race.date == '10-Sep-2021'
        assert race.event == 'Wetherby 10k'
        assert race.url == '/1234'
        assert race.location == 'Wetherby'
        assert race.distance == '10k'
        assert race.type == 'road'


