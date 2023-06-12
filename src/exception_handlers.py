from fastapi import Request
from fastapi.responses import JSONResponse


def attribute_error_handler(request: Request, exc: AttributeError):
    if 'awaitable_attrs' in exc.name:
        return JSONResponse(status_code=400, content={'message': 'Invalid link'})

    raise exc
