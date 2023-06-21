import sys
sys.path.append('../')

import pytest
import src.shorten as shorten


def test_id_to_path():
    assert shorten.id_to_path(314159) == 'mbSV'


def test_path_to_id():
    assert shorten.path_to_id('Q') == 42


def test_path_to_id_value_error():
    # rn not everything besides the reserved characters is acceptable for path_to_id, so this test is definitely subject to change
    with pytest.raises(ValueError):
        shorten.path_to_id('?&')

