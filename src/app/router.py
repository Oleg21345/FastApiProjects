# GET бере дані
# POST створює дані
# PUT оновлює
# DELETE Видаляэ
from fastapi import Body, UploadFile, File
from typing import Annotated
from src.schemas.schema.validate_data import RegisterFild
from src.schemas.schema.response_validate import UserOutId, UserOut
from fastapi import APIRouter
from src.database.metod_for_database import MetodSQL
from src.database.engine import SessionDep
import asyncio
from fastapi.responses import StreamingResponse, FileResponse

# prefix = "/"
router = APIRouter(
    tags = ["Користувачі🧑‍💻"]
)

async def sleep():
    await asyncio.sleep(3)
    print("Add to database some parametr")


@router.post("/users", summary="Реєстрація")
async def register_user(
        session: SessionDep ,user: Annotated[RegisterFild, Body()]
):
    user_add = await MetodSQL.add_user(session,user)
    return {"success": user_add}


@router.put("/users/{user_id}", summary="Змінення")
async def change_user(
        session: SessionDep ,user_id: int,user: RegisterFild
) -> bool:
    user_id = int(user_id)
    user_put = await MetodSQL.change_user(session,user_id,user)
    return user_put

@router.delete("/users/{user_id}", summary="Видалити користувача")
async def delete_user(
        session: SessionDep  ,user_id
) -> bool:
    user_id = int(user_id)
    user_delete = await MetodSQL.delete_user(session,user_id)
    return user_delete

@router.get("/users", summary="Отримати всіх користувачів")
async def get_user(session: SessionDep ) -> list[UserOut]:
    user = await MetodSQL.find_user(session)
    return user


@router.get("/users/{user_id}", summary="Отримати конкретного користувача")
async def user(session: SessionDep ,user_id: int):
    user = await MetodSQL.find_one_user(session, user_id)
    return user



# @router.post("/files")
# async def upload_file(upload_file: UploadFile):
#     file = upload_file.file
#     file_name = upload_file.filename
#     with open(f"1_{file_name}", "wb") as f:
#         f.write(file.read())
#
#
# @router.post("/upload_files")
# async def upload_file(upload_file: list[UploadFile]):
#     for upload in upload_file:
#         file = upload.file
#         file_name = upload.filename
#         with open(f"1_{file_name}", "wb") as f:
#             f.write(file.read())
#
#
# @router.get("/files{file_name}")
# async def get_files(filename: str):
#     return FileResponse(filename)
#
# async def generator(filename):
#     with open(filename, "rb") as f:
#         while chunk:= f.read(1024 * 1024):
#             yield chunk
#
#
# @router.get("/stremeng_files")
# async def stream_file(filename):
#     return StreamingResponse(generator(filename), media_type="video/mp4")


