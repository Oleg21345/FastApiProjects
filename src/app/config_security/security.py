from authx import AuthX, AuthXConfig
from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security_header = HTTPBasic()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_name"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)