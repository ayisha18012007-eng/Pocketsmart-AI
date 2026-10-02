from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, pages, planners
from app.services.config import FRONTEND_ORIGINS
from app.services.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title="PocketSmart AI",
    description=(
        "Generative AI powered personal "
        "planning and recommendation platform."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.get("/health")
def health():

    return {
        "status": "ok",
        "application": "PocketSmart AI",
        "version": "1.0.0"
    }