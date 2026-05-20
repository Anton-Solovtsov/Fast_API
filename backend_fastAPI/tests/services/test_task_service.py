from unittest.mock import Mock

import pytest

from backend_fastAPI.models.models import TaskORM
from backend_fastAPI.schemas.tasks import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from backend_fastAPI.services.exception import TaskNotFoundError
from backend_fastAPI.services.task import TaskService


def test_list_task_returns_pydantic_models(
    service_task: TaskService,
    repository_mock_task: Mock,
) -> None:
    repository_mock_task.get_all.return_value = [
        TaskORM(id="Task_1", title="Изучить pytest", completed=False),
        TaskORM(id="Task_2", title="Написать первый тест", completed=True),
    ]
    result = service_task.list_tasks()

    assert result == [
        TaskSchema(id="Task_1", title="Изучить pytest", completed=False),
        TaskSchema(id="Task_2", title="Написать первый тест", completed=True),
    ]


def test_create_task_commits_create_task(
    service_task: TaskService,
    db_mock: Mock,
    repository_mock_task: Mock,
) -> None:
    create_task = TaskORM(id="Task_1", title="Учить FastAPI", completed=False)

    # repository_mock.create.return_value(create_task)
    repository_mock_task.create.return_value = create_task

    result = service_task.create_task(TaskCreateSchema(title="Учить FastAPI"))
    repository_mock_task.create.assert_called_once_with("Учить FastAPI")
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": "Task_1",
        "title": "Учить FastAPI",
        "completed": False,
    }


@pytest.mark.parametrize(
    "payload, expected_title, expected_completed",
    [
        (TaskUpdateSchema(title="Что то новое"), "Что то новое", False),
        (TaskUpdateSchema(completed=True), "Учить FastAPI", True),
        (
            TaskUpdateSchema(title="Что то новое_3", completed=True),
            "Что то новое_3",
            True,
        ),
        (TaskUpdateSchema(), "Учить FastAPI", False),
    ],
)
def test_update_task_updates_only_passed_fields(
    service_task: TaskService,
    db_mock: Mock,
    repository_mock_task: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="Task_1", title="Учить FastAPI", completed=False)
    repository_mock_task.get_by_id.return_value = task
    result = service_task.update_task(task_id="Task_1", task_update=payload)
    repository_mock_task.get_by_id.assert_called_once_with(task_id="Task_1")
    db_mock.commit.assert_called_once_with()

    assert task.title == expected_title
    assert task.completed == expected_completed

    assert result.model_dump() == {
        "id": "Task_1",
        "title": expected_title,
        "completed": expected_completed,
    }


def test_update_task_raises_task_not_found(
    service_task: TaskService,
    db_mock: Mock,
    repository_mock_task: Mock,
) -> None:
    repository_mock_task.get_by_id.return_value = None
    with pytest.raises(TaskNotFoundError):
        service_task.update_task("missing-task", TaskUpdateSchema(title="Что то"))
    db_mock.commit.assert_not_called()
