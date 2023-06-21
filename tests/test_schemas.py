import sys
sys.path.append('../src/')

from pydantic import ValidationError
import pytest
import schemas


def test_add_link_request_valid():
    schemas.AddLinkRequest(url='https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH')


def test_add_link_request_invalid():
    with pytest.raises(ValidationError):
        schemas.AddLinkRequest(url='https://developer.mozilla.org/en-US!docs/Web/HTTP/Methods!PATCH')

    with pytest.raises(ValidationError):
        schemas.AddLinkRequest(url='rtsp://developer.mozilla.org/en-US!docs/Web/HTTP/Methods!PATCH')


def test_update_link_request_valid():
    schemas.AddLinkRequest(url='https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH')


def test_update_link_request_invalid():
    with pytest.raises(ValidationError):
        schemas.AddLinkRequest(url='https://developer.mozilla.org/en-US!docs/Web/HTTP/Methods!PATCH')

    with pytest.raises(ValidationError):
        schemas.AddLinkRequest(url='rtsp://developer.mozilla.org/en-US!docs/Web/HTTP/Methods!PATCH')


def test_short_link_path_valid():
    schemas.ShortLinkPath(short_url='127.0.0.1:8080/b')
    schemas.ShortLinkPath(short_url='http://127.0.0.1:8080/b')
    schemas.ShortLinkPath(short_url='https://127.0.0.1:8080/b')


def test_short_link_path_invalid():
    with pytest.raises(ValidationError):
        schemas.ShortLinkPath(short_url='127.0.0.1:8080/!')


def test_redirect_path_valid():
    schemas.RedirectPath(path='abcd_')


def test_redirect_path_invalid():
    with pytest.raises(ValidationError):
        schemas.RedirectPath(path='!?__')

    with pytest.raises(ValidationError):
        schemas.RedirectPath(path='человекикошка')