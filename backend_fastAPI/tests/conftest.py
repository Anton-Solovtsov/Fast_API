from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from backend_fastAPI.repositories.category import CategoryRepository
from backend_fastAPI.repositories.task import TaskRepository
from backend_fastAPI.services.category import CategoryService
from backend_fastAPI.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=Session)


@pytest.fixture
def repository_mock_task() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def service_task(db_mock: Mock, repository_mock_task: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.task_repository = repository_mock_task
    return task_service


@pytest.fixture
def repository_mock_category() -> Mock:
    return Mock(spec=CategoryRepository)


@pytest.fixture
def service_category(db_mock: Mock, repository_mock_category: Mock) -> CategoryService:
    category_service = CategoryService(db_mock)
    category_service.category_repository = repository_mock_category
    return category_service
