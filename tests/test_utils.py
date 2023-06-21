import sys
sys.path.append('../')

import src.utils as utils


def test_remove_schema_http_schema_present():
    assert utils.remove_schema('http://da.net') == 'da.net'


def test_remove_schema_https_schema_present():
    assert utils.remove_schema('https://da.net') == 'da.net'


def test_path_from_short_url():
    assert utils.path_from_short_url('da.net/path') == 'path'
    assert utils.path_from_short_url('da.net/path/also_path') == 'also_path'
