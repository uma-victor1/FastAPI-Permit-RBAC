from datetime import timedelta
from os import getenv


DB_CONNECTION_STRING = getenv("DB_CONNECTION_STRING")
COOKIES_KEY_NAME = "session_token"
SESSION_TIME = timedelta(days=30)
HASH_SALT = getenv("HASH_SALT", "SomeRandomStringHere")
SECRET_KEY = getenv("SECRET_KEY", "secret")
PERMIT_API_KEY = getenv("PERMIT_API_KEY")
PERMIT_PDP_URL = getenv("PERMIT_PDP_URL")
