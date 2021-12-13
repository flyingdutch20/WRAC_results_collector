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
    field_index = rb.create_field_index_from_header(headerrow_run)
    assert len(field_index) == 10

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


def test_find_indices_from_header_fields():
    assert False

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
