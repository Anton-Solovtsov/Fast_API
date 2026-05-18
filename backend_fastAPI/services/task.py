from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend_fastAPI.repositories.task import TaskRepository
from backend_fastAPI.schemas.tasks import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema):
        task = self.task_repository.create(task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema):
        task_for_up = self.task_repository.get_by_id(task_id=task_id)
        if task_for_up:
            if task_update.title is not None:
                task_for_up.title = task_update.title
            if task_update.completed is not None:
                task_for_up.completed = task_update.completed
            self.db.commit()
            return TaskSchema.model_validate(task_for_up)
        raise HTTPException(status_code=404, detail="Task not found")

    def delete_task(self, task_id: str) -> None:
        task_for_del = self.task_repository.get_by_id(task_id=task_id)
        if task_for_del:
            self.task_repository.delete(task_for_del)
            self.db.commit()
        else:
            raise HTTPException(status_code=404, detail="Task not found")
