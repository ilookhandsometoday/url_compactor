import re
from pydantic import BaseModel, validator, ValidationError
from fastapi import HTTPException
from shorten import ALPHABET
from config import DOMAIN
from utils import remove_schema

_URL_REGEX = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'


class AddLinkRequest(BaseModel):
    url: str

    @validator('url')
    def validate_url(cls, v):
        if not re.match(_URL_REGEX, v) is not None:
            raise ValueError(f'Not a valid URL. Valid URL is matched by this regex: {_URL_REGEX}')

        return v


class ShortLinkPath(BaseModel):
    short_url: str

    @validator('short_url')
    def validate(cls, v):
        v_without_schema = remove_schema(v)
        service_domain = remove_schema(DOMAIN)
        domain, *path = v_without_schema.split('/')
        if len(path) != 1 or domain != service_domain or not all(map(lambda x: x in ALPHABET, path[0])):
            raise ValueError(f'Incorrect short link format. Correct format is domain name followed by a path parameter consisting only of these symbols {ALPHABET}')

        return v

    # validators don't really work properly if a pydantic model is used as a class-as-a-dependency
    # this is a workaround
    @classmethod
    def depends(cls, short_url: str):
        try:
            return cls(short_url=short_url)
        except ValidationError as e:
            for error in e.errors():
                error['loc'] = ('path', *error['loc'])
            raise HTTPException(422, detail=e.errors())


class RedirectPath(BaseModel):
    path: str

    @validator('path')
    def validate(cls, v):
        if not all(map(lambda x: x in ALPHABET, v)):
            raise ValueError(
                f'Incorrect path format. Correct format is a path parameter consisting only of these symbols {ALPHABET}')

        return v

    # validators don't really work properly if a pydantic model is used as a class-as-a-dependency
    # this is a workaround https://github.com/tiangolo/fastapi/issues/147
    @classmethod
    def depends(cls, path: str):
        try:
            return cls(path=path)
        except ValidationError as e:
            for error in e.errors():
                error['loc'] = ('path', *error['loc'])
            raise HTTPException(422, detail=e.errors())


class ShortLinkResponse(BaseModel):
    short_link: str


class DeleteLinkResponse(BaseModel):
    success: bool


class FullUrlResponse(BaseModel):
    original_link: str