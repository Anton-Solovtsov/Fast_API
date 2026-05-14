from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_fastAPI.api.routers.router import api_router
from backend_fastAPI.models.models import Base
from backend_fastAPI.db.session import engine
from backend_fastAPI.core.config import get_settings


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     print("БД создана")
#     yield



settings = get_settings()
app = FastAPI()
app.include_router(router=api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_methods=["*"],

)
