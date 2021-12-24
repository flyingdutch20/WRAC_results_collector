import pytest

import racebest_utils as rbu
import result
import shelve
import uuid

import config

"""
test store header as shelve
1. what if config doesn't have a label for shelve_path (should be covered by config utils)
2. what if config path is just an empty string
3. test store_header bad input
4. test store_header empty list
5. test store_header one item in list
6. test store_header two items in list
"""

def test_store_header_input_errors(my_date):
    with pytest.raises(TypeError):
        rbu.store_header()
    with pytest.raises(TypeError):
        rbu.store_header("blabla")
