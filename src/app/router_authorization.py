from fastapi import APIRouter, Response, Depends
from src.schemas.schema.validate_data import LoginSchema
from src.database.metod_for_database import MetodSQL
from src.database.engine import SessionDep
from src.database.models.models import security

router = APIRouter(
    tags = ["Реєстрація🧑‍💻"]
)


@router.post("/login")
async def login(session: SessionDep ,creds: LoginSchema, response: Response):
    return await MetodSQL.check_password(session, creds, response)

@router.get("/logout")
async def logout(response: Response):
    return await MetodSQL.logout(response)

@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "TOP SECRET"}
