from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables

from api.controller import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
