from uuid import uuid4
from fastapi import HTTPException
from fastapi import status
from backend_fastAPI.config import app
from backend_fastAPI.db.db_file import (
    Books,
    Categories,
    Tasks)
from backend_fastAPI.models.models import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateSchema
)


@app.get("/")
def get_books():
    return f'Любимые книги: {Books}'


@app.post("book")
def create_book(book: str):
    Books.append(book)
    return book

@app.get('/tasks', status_code=status.HTTP_200_OK)
def get_tasks():
    return Tasks

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreateSchema):
    new_task = TaskSchema(
        id = str(uuid4()),
        title = payload.title,
        completed = False
    )
    Tasks.append(new_task)
    return new_task

@app.patch('/tasks/{task_id}', status_code=status.HTTP_200_OK)
def update_task(task_id, payload:TaskUpdateSchema):
    for task in Tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
    for task in Tasks:
        if task.id == task_id:
            Tasks.remove(task)
            return

@app.get('/categories')
def get_categories():
    return Categories


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreateSchema):
    new_cat = CategorySchema (
        id=str(uuid4()),
        name=payload.name,
    )
    Categories.append(new_cat)
    return new_cat


@app.patch('/categories/{category_id}', status_code=status.HTTP_200_OK)
def update_categories(category_id, payload: CategoryUpdateSchema):
    for cat in Categories:
        if cat.id == category_id:
            cat.name = payload.name
            return cat
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )


@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(category_id):
    for cat in Categories:
        if cat.id == category_id:
            Categories.remove(cat)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found",
    )
