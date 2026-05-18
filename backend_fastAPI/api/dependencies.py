from fastapi import Depends
from sqlalchemy.orm import Session

from backend_fastAPI.db.session import get_db
from backend_fastAPI.services.category import CategoryService
from backend_fastAPI.services.task import TaskService


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
