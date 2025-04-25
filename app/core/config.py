import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
OAUTH2_TOKEN_URL = os.getenv("OAUTH2_TOKEN_URL")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=OAUTH2_TOKEN_URL)
JWT_ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
JWT_ALGO = os.getenv("JWT_ALGO")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS"))
DATABASE_PATH = os.getenv("DATABASE_PATH")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")
