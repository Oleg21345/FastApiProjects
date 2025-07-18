from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import HTTPBasicCredentials
from src.database.metod_for_database import MetodSQL
from src.app.config_security.security import security_header as security
from src.database.engine import SessionDep


router = APIRouter(
    tags=["Реєстрація базова"]
)

@router.get("/basic")
async def register(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hello",
        "username": credentials.username,
        "password": credentials.password
    }



@router.get("/basic-usernames")
async def check_user(
        session: SessionDep,
        creds: Annotated[HTTPBasicCredentials, Depends(security)]
):
    auth_user = await MetodSQL.check_password_basic(session,creds)
    return {
        "message": f"Hi! {auth_user['message']}",
        "username": auth_user['message']
    }



