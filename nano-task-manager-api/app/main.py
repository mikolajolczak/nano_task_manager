from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.database import engine, Base, create_tables

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield
app = FastAPI(lifespan=lifespan)