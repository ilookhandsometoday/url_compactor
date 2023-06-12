from pydantic import BaseModel, validator
from utils import validate_url, URL_REGEX


class LinkRequest(BaseModel):
    url: str

    @validator('url')
    def validate_url(cls, v):
        if not validate_url(v):
            raise ValueError(f'Not a valid URL. Valid URL is matched by this regex: {URL_REGEX}')

        return v


