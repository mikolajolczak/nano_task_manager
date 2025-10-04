from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .comments.controllers import comment_router
from .core.database import engine, Base, create_tables
from .projects.controllers import project_router
from .tags.controllers import tag_router
from .tasks.controllers import task_router
from .users.controllers import user_router

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(comment_router)
app.include_router(project_router)
app.include_router(tag_router)
app.include_router(task_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
