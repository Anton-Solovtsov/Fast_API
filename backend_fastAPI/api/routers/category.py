from fastapi import APIRouter, Depends, status

from backend_fastAPI.api.dependencies import get_category_service
from backend_fastAPI.schemas.categories import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from backend_fastAPI.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", status_code=status.HTTP_200_OK)
def get_categories(
    category_service: CategoryService = Depends(get_category_service),
) -> list[CategorySchema]:
    return category_service.list_category()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_task(
    category_id,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.update_category(category_id=category_id, cat_update=payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    category_id, category_service: CategoryService = Depends(get_category_service)
):
    return category_service.delete_category(category_id=category_id)
