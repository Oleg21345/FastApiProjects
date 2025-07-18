from .engine import AsyncSession
from sqlalchemy import select
import logging
from src.schemas.schema.validate_data import RegisterFild, LoginSchema
from fastapi import HTTPException, Response
from src.database.models.models import RegisterUser
from src.schemas.schema.response_validate import UserOut, UserOutId
from fastapi import Depends
from typing import Annotated
from fastapi.security import HTTPBasicCredentials
from src.app.config_security.security import security_header as security
from src.app.config_security.security import config

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


likes_memory = {}
class MetodSQL:

    @staticmethod
    async def add_user(session: AsyncSession, data: RegisterFild) -> int:
        await RegisterUser.validate_passwords(data.password, data.password_repeat)
        print(f"Data {data.password}")
        hashed_password = await RegisterUser.set_password(data.password)
        user = RegisterUser(
            name=data.name,
            age=data.age,
            email=data.email,
            password=hashed_password
        )

        session.add(user)
        await session.flush()
        await session.commit()
        return user.id

    @staticmethod
    async def check_password(session: AsyncSession, creds: LoginSchema, response: Response):
        result = await session.execute(
            select(RegisterUser).where(RegisterUser.name == creds.name)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")


        checked = await RegisterUser.check(user.id , user.password, creds.password, response)
        if checked:
            return checked
        raise HTTPException(status_code=401, detail="Неправильний пароль або юзернейм")


    @staticmethod
    async def logout(response: Response):
        response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
        return {"message": True}


    @staticmethod
    async def check_token(session: AsyncSession,  token: str) -> int:
        result = await session.execute(
            select(RegisterUser).where(RegisterUser.id == int(token))
        )
        user = result.scalars().first()

        if user is None:
            print(f"User {user}")
            raise HTTPException(status_code=404, detail="Користувача не знайдено")

        if user.id != int(token):
            raise HTTPException(status_code=403, detail="Недійсний токен")

        return user.id


    @staticmethod
    async def check_password_basic(session: AsyncSession,
                                    creds: Annotated[HTTPBasicCredentials, Depends(security)]):
        result = await session.execute(
            select(RegisterUser).where(RegisterUser.name == creds.username)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")

        print(f"User password in db {user.password}")
        print(f"Password search {creds.password}")
        checked = await RegisterUser.check_header_basic(user.password, creds.password)
        if checked:
            return {"message": user.name}
        raise HTTPException(status_code=401, detail="Неправильний пароль або юзернейм")

    @staticmethod
    async def change_user(
        session: AsyncSession,user_id: int,data: RegisterFild
        ):
        user = await session.execute(
            select(RegisterUser).where(RegisterUser.id == user_id)
        )
        res = user.scalars().first()
        print(f"User {user}")
        print(f"Result {res}")
        if not res:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items(): # key поле в котрому треба міняти значення
            # value нове значення для цього поля
            setattr(res,key, value)

        print("Commit")
        await session.commit()
        print("True")
        return True

    @staticmethod
    async def delete_user(session: AsyncSession,user_id):
        query = await session.execute(
            select(RegisterUser).where(RegisterUser.id == user_id)
        )
        res = query.scalars().first()
        await session.delete(res)
        await session.commit()
        return True

    @staticmethod
    async def find_user(session: AsyncSession) -> list[UserOut]:
        query = await session.execute(
            select(RegisterUser)
        )
        res = query.scalars().all()
        register_schema = [UserOut.model_validate(reg) for reg in res]
        return register_schema

    @staticmethod
    async def find_one_user(session: AsyncSession,user_id) -> UserOutId:
        query = await session.execute(
            select(RegisterUser).where(RegisterUser.id == user_id)
        )
        res = query.scalars().first()
        if res:
            return UserOutId.model_validate(res)
        else:
            raise HTTPException(status_code=404, detail="Користувача під таким айді не існує")

