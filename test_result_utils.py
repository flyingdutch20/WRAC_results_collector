import pytest
import os
import config

import result_utils as rbu
import result
import shelve
import uuid

import config

@pytest.fixture(scope='session')
def temp_dir(tmp_path_factory):
    file_path = tmp_path_factory.mktemp('yaml')
    return file_path

@pytest.fixture(scope="session")
def config_yaml(temp_dir):
    filename = os.path.join(temp_dir, 'config.yml')
    fileobj = open(filename,'w')
    fileobj.write("shelves:\n")
    fileobj.write(f" racebest_headers: {temp_dir}/headerrows\n")
    fileobj.close()
    return filename


"""
test store header as shelve
1. what if config doesn't have a label for shelve_path (should be covered by config utils)
2. what if config path is just an empty string
3. test store_header bad input
4. test store_header empty list
5. test store_header one item in list
6. test store_header two items in list
"""

def test_store_header_input_errors(config_yaml):
    with pytest.raises(TypeError):
        rbu.store_racebest_header(None, config_yaml)
    with pytest.raises(TypeError):
        rbu.store_racebest_header("blabla", config_yaml)

@pytest.mark.parametrize(
    'items',
    [
        ([]),
        (['one']),
        (['one','two']),
        (['one','two','three']),
    ],
)
def test_store_header_multiple(config_yaml,items):
    rbu.store_racebest_header(items, config_yaml)
    shelve_path = config.racebest_headers_shelve(config_yaml)
    with shelve.open(shelve_path) as book:
        my_list = list(book.values())[0]
        assert len(my_list) == len(items)

def test_store_header_new_book_every_time(config_yaml):
    rbu.store_racebest_header((['one', 'two', 'three']), config_yaml)
    rbu.store_racebest_header((['new']), config_yaml)
    shelve_path = config.racebest_headers_shelve(config_yaml)
    with shelve.open(shelve_path) as book:
        my_list = list(book.values())[0]
        assert len(my_list) == 1
        assert my_list[0] == 'new'
