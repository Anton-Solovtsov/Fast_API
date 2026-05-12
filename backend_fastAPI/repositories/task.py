from sqlalchemy import select

from backend_fastAPI.models.models import TaskORM


class TaskRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self) -> TaskORM:
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM:
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) ->TaskORM:
        task = TaskORM(
            title=title,
            completed=False
        )
        self.db.add(task)
        return task

    def delete(self, TaskORM) -> None:
        self.db.delete(TaskORM)


