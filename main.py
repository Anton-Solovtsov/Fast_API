from uuid import uuid4
from fastapi import HTTPException, Depends
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend_fastAPI.config import app, get_db
from backend_fastAPI.db.db_file import (
    Categories,
    Tasks,
    TaskORM,
    CategoryORM
)
from backend_fastAPI.models.models import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateSchema
)

def task_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
        id = task_orm.id,
        title = task_orm.title,
        completed = task_orm.completed
    )

@app.get('/tasks', status_code=status.HTTP_200_OK, response_model=Tasks)
def get_tasks(db: Session = Depends(get_db)) ->list[TaskSchema]:
    tasks = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks]

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreateSchema, db: Session = Depends(get_db)):
    new_task = TaskORM(
        title = payload.title,
        completed = False
    )
    db.add(new_task)
    db.commit()
    return task_to_model(new_task)

@app.patch('/tasks/{task_id}', status_code=status.HTTP_200_OK)
def update_task(task_id, payload:TaskUpdateSchema, db: Session = Depends(get_db)):
    task_db = db.get(TaskORM, task_id)

    if payload.title:
        task_db.title = payload.title
    if payload.completed is not None:
        task_db.completed = payload.completed
    db.commit()
    return task_db

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)):
    task_db = db.get(TaskORM, task_id)
    db.delete(task_db)
    db.commit()
    return


def category_to_model(cat_orm: CategoryORM):
    return CategorySchema(
        id = cat_orm.id,
        name = cat_orm.name
    )


@app.get('/categories')
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryORM))
    return [category_to_model(cat) for cat in categories]


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreateSchema, db: Session = Depends(get_db)):
    new_cat = CategoryORM(
        name=payload.name
    )
    db.add(new_cat)
    db.commit()
    return category_to_model(new_cat)


@app.patch('/categories/{category_id}', status_code=status.HTTP_200_OK)
def update_categories(category_id, payload: CategoryUpdateSchema, db: Session = Depends(get_db)):
    try:
        update_cat = db.get(CategoryORM, category_id)
        update_cat.name = payload.name
        db.commit()
        return update_cat
    except:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(category_id, db: Session = Depends(get_db)):
    try:
        del_cat = db.get(CategoryORM, category_id)
        db.delete(del_cat)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
