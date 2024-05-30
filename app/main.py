from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.common.database import create_indexes
from app.routes.user import router as user_router
from app.common.logging.logger import mongo_logger
from app.routes.session import router as session_router
from app.routes.uploadfile import router as uploadfile_router
from app.common.middleware.fastapi_middlewar import Middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_logger.info("Starting up...")
    await create_indexes()
    yield
    mongo_logger.info("Shutting down...")


app = FastAPI(
    title="docViz",
    summary="",
    description="",
    version="0.1",
    openapi_tags=[
        {
            "name": "",
            "description": "",
        },
        {
            "name": "",
            "description": "",
        },
    ],
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(Middleware)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(session_router, prefix="/sessions", tags=["sessions"])
app.include_router(uploadfile_router, prefix="/files", tags=["files"])

@app.get("/")
async def root():
    return JSONResponse(content="Welcome to mdocViz API's")


@app.get("/check_health")
async def check_health():
    return JSONResponse(content="Healthy")
