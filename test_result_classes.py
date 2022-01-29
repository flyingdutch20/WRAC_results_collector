import pytest

import result

class TestResult():
    def test_access_result(self):
        res = result.Result('1','123','Jopie','','','WRAC','M','25','MSEN','22/12/2021','W10K','','Wetherby','10k','',run='3600')
        assert res.pos == '1'
        assert res.bib == '123'
        assert res.name == 'Jopie'
        assert res.club == 'WRAC'
        assert res.gender == 'M'
        assert res.age == "25"
        assert res.category == 'MSEN'
        assert res.date == '22/12/2021'
        assert res.race == 'W10K'
        assert res.distance == '10k'  # 5k, 5M, 10k, 1/2 marathon, marathon, sprint, olympic
        assert res.comment == ''
        assert res.swim == ''
        assert res.t1 == ''
        assert res.bike == ''
        assert res.t2 == ''
        assert res.run == "3600"


class TestRace():
    def test_access_race(self):
        race = result.Race('10-Sep-2021','Wetherby 10k','/1234','Wetherby','10k','road')
        assert race.date == '10-Sep-2021'
        assert race.event == 'Wetherby 10k'
        assert race.url == '/1234'
        assert race.location == 'Wetherby'
        assert race.distance == '10k'
        assert race.type == 'road'


