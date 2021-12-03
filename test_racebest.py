import pytest
from datetime import date

import racebest as rb


def test_get_index():
    with open('test-pages/racebest/index.html', "r") as file:
        page = file.read()
    index = rb.get_races(page, date.fromisoformat('2021-05-01'))
    assert len(index) == 18  # add assertion here

def test_get_runners():
    with open('test-pages/racebest/result_run.html', "r") as file:
        page = file.read()
    runners = rb.parse_race(page)
    assert len(runners) == 118  # add assertion here

def test_get_tri_runners():
    with open('test-pages/racebest/result_tri.html', "r") as file:
        page = file.read()
    tri_runners = rb.parse_race(page)
    assert len(tri_runners) == 107  # add assertion here
