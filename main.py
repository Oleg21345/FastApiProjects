from fastapi import Request
from src.app import global_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Callable
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.database.config import settings
from src.database.create_tables import create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(settings.DATABASE_URL_asyncpg)
    app.state.engine = engine
    app.state.sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    yield
    await create_table(engine)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(global_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"]

)

@app.middleware("http")
async def my_middleware(request: Request, call_next: Callable):
    ip_address = request.client.host
    print(f"Ip address {ip_address}")

    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f"Час обробки запиту становить {end}")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
