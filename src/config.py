import os

HOST: str = os.getenv('URL_COMPACTOR_HOST') or '127.0.0.1'
PORT: int = int(os.getenv('URL_COMPACTOR_PORT')) or 8000
DOMAIN: str = os.getenv('URL_COMPACTOR_DOMAIN') or f'{HOST}:port'
DATABASE_URL: str = os.getenv('URL_COMPACTOR_DATABASE')
if not DATABASE_URL:
    raise LookupError('Nothing in URL_COMPACTOR_DATABASE environment variable (or the env var is not set)')