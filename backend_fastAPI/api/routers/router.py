from fastapi import APIRouter
from backend_fastAPI.api.routers.task import router as task_router
from backend_fastAPI.api.routers.category import router as category_router

api_router = APIRouter()
api_router.include_router(task_router)
api_router.include_router(category_router)