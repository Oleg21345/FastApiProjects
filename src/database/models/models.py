from src.database.engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from fastapi import HTTPException, Response
import bcrypt
from src.app.config_security.security import security, config



class RegisterUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    email: Mapped[str]
    password: Mapped[str]


    @staticmethod
    async def set_password(plain_text_password: str):
        hashed_password = bcrypt.hashpw(
            plain_text_password.encode("utf-8"),
            bcrypt.gensalt()
        )
        password_hash = hashed_password.decode("utf-8")
        return password_hash

    @staticmethod
    async def check(user_id,password,attempted_password: str, response: Response):
        check = bcrypt.checkpw(
            attempted_password.encode("utf-8"),
            password.encode("utf-8")
        )
        if check is True:
            token = security.create_access_token(uid=str(user_id))
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access": token}
        raise HTTPException(status_code=401, detail="Некоректне ім'я або пароль")

    @staticmethod
    async def check_header_basic(stored_hash,
                                   attempted_password: str
                                   ):
        check = bcrypt.checkpw(
            attempted_password.encode("utf-8"),
            stored_hash.encode("utf-8")
        )
        if check is True:
            print("Correct")
            return True
        print("ancorrect")
        raise HTTPException(status_code=401, detail="Некоректне ім'я або пароль")

    @staticmethod
    async def validate_passwords(password,password_repeat):
        if password != password_repeat:
            raise ValueError("Passwords do not match")
