import os

HOST: str = os.getenv('URL_COMPACTOR_HOST') or '127.0.0.1'
PORT: int = int(os.getenv('URL_COMPACTOR_PORT')) or 8000
# domain as in the domain that will be returned to the user as a part of the short link, so it has to be a domain
# that points to this particular service
DOMAIN: str = os.getenv('URL_COMPACTOR_DOMAIN') or f'{HOST}:{PORT}'
DATABASE_URL: str = os.getenv('URL_COMPACTOR_DATABASE')
if not DATABASE_URL:
    raise LookupError('Nothing in URL_COMPACTOR_DATABASE environment variable (or the env var is not set)')