from sqlalchemy import select
from sqlalchemy.orm import Session

from backend_fastAPI.models.models import CategoryORM


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, name):
        new_cat=CategoryORM(name=name)
        self.db.add(new_cat)
        return new_cat

    def delete(self, category: CategoryORM):
        self.db.delete(category)

