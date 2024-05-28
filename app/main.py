from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.common.logging.logger import file_logging
from app.common.middleware.fastapi_middlewar import Middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    file_logging.info("Starting up...")
    yield
    file_logging.info("Shutting down...")


app = FastAPI(
    title="",
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
app.include_router()



@app.get("/")
async def root():
    return JSONResponse(content="Welcome to  API's")


@app.get("/check_health")
async def check_health():
    return JSONResponse(content="Healthy")
