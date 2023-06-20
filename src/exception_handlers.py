from fastapi import Request
from fastapi.responses import JSONResponse


def attribute_error_handler(request: Request, exc: AttributeError):
    """An exception handler for a specific flavour of an attribute error - the one that happens when there is an attempt
    to read an attr from a None object (that usually hapens when session.get(Class, id) is used, and a row with id is
    nonexistent"""
    if 'awaitable_attrs' in exc.name:
        return JSONResponse(status_code=400, content={'message': 'Invalid short link'})

    raise exc
