from sqlalchemy.orm import Session

from backend_fastAPI.repositories.category import CategoryRepository
from backend_fastAPI.schemas.categories import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from backend_fastAPI.services.exception import CategoryNotFoundError


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_category(self) -> list[CategorySchema]:
        cat_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(cat) for cat in cat_orm]

    def create_category(self, category_create: CategoryCreateSchema):
        new_cat = self.category_repository.create(category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(new_cat)

    def update_category(self, category_id: str, cat_update: CategoryUpdateSchema):
        cat_for_up = self.category_repository.get_by_id(category_id=category_id)
        if cat_for_up:
            if cat_update.name is not None:
                cat_for_up.name = cat_update.name
            self.db.commit()
            return CategorySchema.model_validate(cat_for_up)
        raise CategoryNotFoundError(status_code=404, detail="Category not found")

    def delete_category(self, category_id: str) -> None:
        cat_for_del = self.category_repository.get_by_id(category_id=category_id)
        if cat_for_del:
            self.category_repository.delete(cat_for_del)
            self.db.commit()
        else:
            raise CategoryNotFoundError(status_code=404, detail="Category not found")
