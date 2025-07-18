from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from fastapi import Request, Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from typing import Annotated

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

def get_sessionmaker(request: Request) -> async_sessionmaker:
    return request.app.state.sessionmaker

async def get_session(
    sessionmaker: async_sessionmaker = Depends(get_sessionmaker)
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
