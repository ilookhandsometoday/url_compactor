import sys
sys.path.append('../')

import src.shorten as shorten


def test_id_to_path():
    assert shorten.id_to_path(314159) == 'mbSV'


def test_path_to_id():
    assert shorten.path_to_id('Q') == 42
