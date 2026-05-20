from unittest.mock import Mock

import pytest

from backend_fastAPI.models.models import CategoryORM
from backend_fastAPI.schemas.categories import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from backend_fastAPI.services.category import CategoryService
from backend_fastAPI.services.exception import CategoryNotFoundError


def test_list_category(
    service_category: CategoryService,
    repository_mock_category: Mock,
) -> None:

    repository_mock_category.get_all.return_value = [
        CategoryORM(id="str_1", name="Category_1"),
        CategoryORM(id="str_2", name="Category_2"),
    ]

    result = service_category.list_category()

    assert result == [
        CategorySchema(id="str_1", name="Category_1"),
        CategorySchema(id="str_2", name="Category_2"),
    ]


def test_create_category_commits_create_category(
    service_category: CategoryService, repository_mock_category: Mock, db_mock: Mock
) -> None:

    create_category = CategoryORM(id="str_1", name="Category_1")
    repository_mock_category.create.return_value = create_category

    result = service_category.create_category(CategoryCreateSchema(name="Category_1"))
    repository_mock_category.create.assert_called_once_with("Category_1")
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": "str_1",
        "name": "Category_1",
    }


@pytest.mark.parametrize(
    "payload, expected_name",
    [
        (CategoryCreateSchema(name="Что то новое"), "Что то новое"),
    ],
)
def test_update_category(
    service_category: CategoryService,
    db_mock: Mock,
    repository_mock_category: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    cat = CategoryORM(id="num_1", name="Что то про категорию")
    repository_mock_category.get_by_id.return_value = cat

    result = service_category.update_category(category_id="num_1", cat_update=payload)
    repository_mock_category.get_by_id.assert_called_once_with(category_id="num_1")
    db_mock.commit.assert_called_once_with()

    assert cat.name == expected_name

    assert result.model_dump() == {
        "id": "num_1",
        "name": expected_name,
    }


def test_update_category_raises_category_not_found(
    service_category: CategoryService,
    db_mock: Mock,
    repository_mock_category: Mock,
) -> None:
    repository_mock_category.get_by_id.return_value = None
    with pytest.raises(CategoryNotFoundError):
        service_category.update_category(
            "missing-cat", CategoryUpdateSchema(name="Что то")
        )
    db_mock.commit.assert_not_called()
