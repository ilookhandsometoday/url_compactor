import os

HOST: str = os.getenv('URL_COMPACTOR_HOST') or '127.0.0.1'
PORT: int = 8080
try:
    PORT = int(os.getenv('URL_COMPACTOR_PORT'))
except:
    pass
# domain as in the domain that will be returned to the user as a part of the short link, so it has to be a domain
# that points to this particular service
DOMAIN: str = os.getenv('URL_COMPACTOR_DOMAIN') or f'{HOST}:{PORT}'
DATABASE_URL: str = os.getenv('URL_COMPACTOR_DATABASE') or 'postgresql+asyncpg://myuser:mypassword@localhost/mydb'
