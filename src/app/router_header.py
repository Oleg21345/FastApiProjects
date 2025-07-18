from fastapi import Header
from fastapi import APIRouter
from src.database.metod_for_database import MetodSQL
from src.database.engine import SessionDep

router = APIRouter(
    tags=["Заголовки"]
)


@router.get("/headers")
async def check_user(
        session: SessionDep,
        auth_token:str = Header(alias="x-auth-token")
):
    user = await MetodSQL.check_token(session, auth_token)
    return {
        "message": f"Welcome, {user}!",
        "user_id": user
    }

#
