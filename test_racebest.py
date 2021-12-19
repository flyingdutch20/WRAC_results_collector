import pytest
from bs4 import BeautifulSoup as bs
from datetime import date

import racebest as rb
import result


@pytest.fixture()
def headerrow_run():
    headerrow = '<tr><th> <span class="visible-phone">Pos.</span><span class="hidden-phone">Position</span></th><th class="hidden-phone">Bib</th><th> <span class="visible-phone">Name</span><span class="hidden-phone">Name</span></th><th class="hidden-phone">Club</th><th class="hidden-phone hidden-tablet">Wave</th><th class="hidden-phone hidden-tablet">Age Grade</th><th class="hidden-phone hidden-tablet">Category</th><th class="hidden-phone hidden-tablet">Category Position</th><th> <span class="visible-phone">Net Time</span><span class="hidden-phone">Net Time</span></th><th><span class="hidden-phone">Share</span></th></tr>'
    return bs(headerrow, "html.parser")

def test_create_field_index_from_header(headerrow_run):
    field_index = rb.create_field_index_from_header(headerrow_run,False)
    assert isinstance(field_index,dict)

class TestExtractHeaderFields():
    def test_extract_header_fields_no_param(self):
        with pytest.raises(TypeError):
            rb.extract_header_fields()

    def test_extract_header_fields_bad_input(self):
        with pytest.raises(AttributeError):
            rb.extract_header_fields("bad")

    def test_extract_header_fields_no_th(self):
        headerrow = '<tr>nothing</tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == []

    def test_extract_header_fields_one_empty_th(self):
        headerrow = '<tr><th></th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == []

    def test_extract_header_fields_two_empty_th(self):
        headerrow = '<tr><th></th><th></th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == []

    def test_extract_header_fields_no_span(self):
        headerrow = '<tr><th>my text</th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == ['my text']

    def test_extract_header_fields_one_span(self):
        headerrow = '<tr><th class="hidden-phone">Club</th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == ['Club']

    def test_extract_header_fields_two_span(self):
        headerrow = '<tr><th> <span class="visible-phone">Pos.</span><span class="hidden-phone">Position</span></th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == ['Position']

    def test_extract_header_fields_more_than_two_span(self):
        headerrow = '<tr><th> <span class="visible-phone">Pos.</span><span class="hidden-phone">Position</span><span class="visible-tablet">T-Pos.</span><span class="hidden-tablet">No-T Pos.</span></th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == ['Position']

    def test_extract_header_fields_multi(self):
        headerrow = '<tr><th> <span class="visible-phone">Pos.</span><span class="hidden-phone">Position</span></th><th class="hidden-phone">Bib</th>' \
                    '<th> <span class="visible-phone">Name</span><span class="hidden-phone">Name</span></th><th class="hidden-phone">Club</th>' \
                    '<th class="hidden-phone hidden-tablet">Wave</th><th class="hidden-phone hidden-tablet">Age Grade</th>' \
                    '<th class="hidden-phone hidden-tablet">Category</th><th class="hidden-phone hidden-tablet">Category Position</th>' \
                    '<th> <span class="visible-phone">Net Time</span><span class="hidden-phone">Net Time</span></th><th><span class="hidden-phone">Share</span></th></tr>'
        result =  rb.extract_header_fields(bs(headerrow, "html.parser"))
        assert result == ['Position','Bib','Name','Club','Wave','Age Grade','Category','Category Position','Net Time','Share']


class TestFindIndicesFromHeaderFields():
    def test_find_indices_from_header_fields_no_param(self):
        # 1. bad input; no list
        with pytest.raises(TypeError):
            rb.find_indices_from_header_fields()

    def test_find_indices_from_header_fields_bad_input(self):
        # 1. bad input; no list
        with pytest.raises(AssertionError):
            rb.find_indices_from_header_fields("bad")

    def test_find_indices_from_header_fields_empty_list(self):
        # 2. empty list
        result = rb.find_indices_from_header_fields([])
        assert isinstance(result, dict)

    def test_find_indices_from_header_fields_single_element(self):
        # 3. list with 1 element
        result = rb.find_indices_from_header_fields(['whatever'])
        assert isinstance(result, dict)

    def test_find_indices_from_header_fields_first_always_position(self):
        # 4. 1st always 'pos'
        result = rb.find_indices_from_header_fields(['position','abc','position','def','age position'])
        assert result['pos'] == 0
        result = rb.find_indices_from_header_fields(['nothing','abc','position','def','age position'])
        assert result['pos'] is None

    def test_find_indices_from_header_fields_find_bib(self):
        # 5. find 'bib', 'Bib', 'BIB', 'Race Number', 'Bib Number'
        result = rb.find_indices_from_header_fields(['whatever','bib','position','def','age position'])
        assert result['bib'] == 1
        result = rb.find_indices_from_header_fields(['whatever','abc','def','Bib','position','def','age position'])
        assert result['bib'] == 3
        result = rb.find_indices_from_header_fields(['whatever','abc','bib','position','def','age position'])
        assert result['bib'] == 2
        result = rb.find_indices_from_header_fields(['whatever','Bibber','position','def','age position','Bib'])
        assert result['bib'] == 5
        result = rb.find_indices_from_header_fields(['whatever','BIB','position','def','age position'])
        assert result['bib'] == 1
        result = rb.find_indices_from_header_fields(['whatever','Race','position','Race Number','age position'])
        assert result['bib'] == 3
        result = rb.find_indices_from_header_fields(['whatever','position','Bib Number','age position'])
        assert result['bib'] == 2
        result = rb.find_indices_from_header_fields(['whatever','position','Bibber Number','age position'])
        assert result['bib'] is None

    def test_find_indices_from_header_fields_find_name(self):
        # 6. find 'Name'
        result = rb.find_indices_from_header_fields(['whatever','bib','position','name','age position'])
        assert result['name'] == 3
        result = rb.find_indices_from_header_fields(['whatever','Bib','Name','Club Name','Race Name'])
        assert result['name'] == 2
        result = rb.find_indices_from_header_fields(['whatever','Race Name','Club Name','Time','Name','def','age position'])
        assert result['name'] == 4

    def test_find_indices_from_header_fields_find_gender(self):
        # 7. find 'Gender', 'Sex' make sure not 'Gender Category', 'Gender Position'
        result = rb.find_indices_from_header_fields(['whatever','bib','Gender position','Gender','age position'])
        assert result['gender'] == 3
        result = rb.find_indices_from_header_fields(['whatever','Bib','Sex','Gender Category','Race Name'])
        assert result['gender'] == 2
        result = rb.find_indices_from_header_fields(['whatever','Gender Position','Gender Category','Time','Gender','def','age position'])
        assert result['gender'] == 4

    def test_find_indices_from_header_fields_find_category(self):
        # 8. find 'Category', 'Cat', 'Age Category' make sure not 'Category Position'
        result = rb.find_indices_from_header_fields(['whatever','bib','Gender position','Category','age position'])
        assert result['category'] == 3
        result = rb.find_indices_from_header_fields(['whatever','Bib','Cat','Category Position','Race Name'])
        assert result['category'] == 2
        result = rb.find_indices_from_header_fields(['whatever','Category Position','Time','Gender','Gender Category','def','age position'])
        assert result['category'] == 4
        result = rb.find_indices_from_header_fields(['whatever','Category Position','Time','Age Category','Gender','def','age position'])
        assert result['category'] == 3

    def test_find_indices_from_header_fields_find_time(self):
        # 9. find 'Time', 'TIME', 'Net Time', 'Finish Time', 'Chip Time'. If multiple, then order 'Chip Time', 'Net Time', 'Finish Time', 'Time'
        result = rb.find_indices_from_header_fields(['Pos', 'Category Position', 'Time'])
        assert result['time'] == 2
        result = rb.find_indices_from_header_fields(['Pos', 'TIME', 'Age Category', 'Gender', 'def', 'age position'])
        assert result['time'] == 1
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Age Category', 'Net Time', 'def', 'age position'])
        assert result['time'] == 3
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Age Category', 'def', 'Finish Time', 'age position'])
        assert result['time'] == 4
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Age Category', 'Chip Time', 'age position', 'Chip Time'])
        assert result['time'] == 3
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Time', 'Finish Time', 'Net Time', 'Chip Time'])
        assert result['time'] == 5
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Time', 'Finish Time', 'Net Time'])
        assert result['time'] == 4
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Chip Time', 'Finish Time', 'Net Time', 'Chip Time'])
        assert result['time'] == 2

    def test_find_indices_from_header_fields_find_triathlon(self):
        # 10. if Triathlon: Swim,T1,Bike,T2,Run,Finish Time/Swim Incl Run,T1,Bike,T2,Run,Time,
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Swim', 'T1', 'Bike', 'T2', 'Run', 'Finish Time'])
        assert result['swim'] == 2
        assert result['t1'] == 3
        assert result['bike'] == 4
        assert result['t2'] == 5
        assert result['run'] == 6
        assert result['time'] == 7
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Swim', 'T1', 'Bike', 'T2', 'Run', 'Total Time'])
        assert result['time'] == 7
        result = rb.find_indices_from_header_fields(['Pos', 'abc', 'Swim', 'T1', 'Bike', 'T2', 'Run', 'Time'])
        assert result['time'] == 7

    def test_find_indices_from_header_fields_find_club(self):
        # 11. find 'Club', 'Club / Sponsor', 'Club Name', 'Team', 'Team Name'. If both Club and Team then Club prevails
        result = rb.find_indices_from_header_fields(['whatever','position','Club','age position'])
        assert result['club'] == 2
        result = rb.find_indices_from_header_fields(['whatever','Bib','Name','Club Name','Race Name'])
        assert result['club'] == 3
        result = rb.find_indices_from_header_fields(['whatever','Bib','Name','Time', 'Team','Race Name'])
        assert result['club'] == 4
        result = rb.find_indices_from_header_fields(['whatever','Race Name','Club', 'Team Name','Time','Name','def','age position'])
        assert result['club'] == 2


def test_create_runner(race, field_index, fields):
    assert False


def test_get_index():
    with open('test-pages/racebest/index.html', "r") as file:
        page = file.read()
    index = rb.get_races(page, date.fromisoformat('2021-05-01'))
    assert len(index) == 18  # add assertion here

def test_get_runners():
    with open('test-pages/racebest/result_run.html', "r") as file:
        page = file.read()
    race = result.Race()
    runners = rb.parse_race(page, race)
    assert len(runners) == 118  # add assertion here

def test_get_tri_runners():
    with open('test-pages/racebest/result_tri.html', "r") as file:
        page = file.read()
    race = result.Race()
    tri_runners = rb.parse_race(page, race)
    assert len(tri_runners) == 107  # add assertion here
