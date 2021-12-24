import pytest
import os

import config

@pytest.fixture(scope='session')
def temp_dir(tmp_path_factory):
    file_path = tmp_path_factory.mktemp('yaml')
    return file_path

@pytest.fixture(scope="session")
def empty_yaml(temp_dir):
    filename = os.path.join(temp_dir, 'empty.yml')
    fileobj = open(filename,'w')
    fileobj.close()
    return filename

@pytest.fixture(scope="session")
def bad_yaml_nonsense(temp_dir):
    filename = os.path.join(temp_dir, 'bad_nonsense.yml')
    fileobj = open(filename,'w')
    fileobj.write("nonsense\nnonsense\n\nmore nonsense\\n")
    fileobj.close()
    return filename

@pytest.fixture(scope="session")
def bad_yaml_one_level(temp_dir):
    filename = os.path.join(temp_dir, 'bad_one_level.yml')
    fileobj = open(filename,'w')
    fileobj.write("first: first\n")
    fileobj.write(" nonsense\nnonsense\n\nmore nonsense\n")
    fileobj.close()
    return filename

@pytest.fixture(scope="session")
def bad_yaml_three_levels(temp_dir):
    filename = os.path.join(temp_dir, 'bad_three_levels.yml')
    fileobj = open(filename,'w')
    fileobj.write("first:\n")
    fileobj.write(" second:\n")
    fileobj.write("  third: third\n")
    fileobj.close()
    return filename

@pytest.fixture(scope="session")
def good_yaml(temp_dir):
    filename = os.path.join(temp_dir, 'good.yml')
    fileobj = open(filename,'w')
    fileobj.write("first:\n")
    fileobj.write(" second: 2nd\n")
    fileobj.close()
    return filename

"""
test read_yaml_file
1. test file doesn't exist
2. test file is just an empty file
3. test file is a proper configured yaml file
"""

def test_read_yaml_file_no_file():
    with pytest.raises(TypeError):
        config.read_yaml_file()

def test_read_empty_yaml_file(empty_yaml):
    assert not config.read_yaml_file(empty_yaml)

def test_read_good_yaml_file(good_yaml):
    assert config.read_yaml_file(good_yaml)


"""
test read_config
1. test file doesn't exist
2. test file is empty
3. test yaml_file is None
4. test param is bad input (None, only 1, more than 2)
5. test param doesn't exist in config file
6. test param does exist in config file
"""

def test_read_config_file_not_exist():
    result = config.read_config('no_file',('first','second'))
    assert result == ''

def test_read_config_empty_file(empty_yaml):
    result = config.read_config(empty_yaml,('first','second'))
    assert result == ''

def test_read_config_bad_params(good_yaml):
    with pytest.raises(TypeError):
        config.read_config(good_yaml)
    with pytest.raises(IndexError):
        config.read_config(good_yaml,())
    with pytest.raises(KeyError):
        config.read_config(good_yaml,('first'))
    result = config.read_config(good_yaml,('first','second','third'))
    assert not isinstance(result, tuple)

def test_read_config_bad_file_param(bad_yaml_nonsense):
    result = config.read_config(bad_yaml_nonsense,('first','second'))
    assert result == ''

def test_read_config_bad_file_one_level(bad_yaml_one_level):
    result = config.read_config(bad_yaml_one_level,('first','second'))
    assert result == ''

def test_read_config_bad_file_three_levels(bad_yaml_three_levels):
    result = config.read_config(bad_yaml_three_levels,('first','second'))
    assert not isinstance(result, tuple)

def test_read_config_good_file_wrong_key(good_yaml):
    with pytest.raises(KeyError):
        config.read_config(good_yaml,('something','else'))

def test_read_config_correct(good_yaml):
    result = config.read_config(good_yaml,('first','second'))
    assert result == '2nd'
