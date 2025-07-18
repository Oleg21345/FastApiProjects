from .engine import Base
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_table(engine: AsyncEngine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # якщо потрібно
        await conn.run_sync(Base.metadata.create_all)