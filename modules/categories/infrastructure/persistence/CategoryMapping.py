# modules/categories/infrastructure/persistence/CategoryMapping.py
from shared.extensions import db
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping
from modules.categories.domain.Category import Category

class CategoryMapping(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)

    # Relación muchos-a-uno con Area
    area_id = db.Column(db.Integer, db.ForeignKey('area.id_area'), nullable=False)
    area = db.relationship('AreaMapping', backref=db.backref('categories', lazy=True))

    def to_domain(self) -> Category:

        return Category(
            category_id=self.category_id,
            area_id=self.area_id,
            category_name=self.category_name,
            description=self.description,
            price=self.price
        )

    @classmethod
    def from_domain(cls, category: Category):
        return cls(
            category_id=category.category_id,
            area_id=category.area_id,
            category_name=category.category_name,
            description=category.description,
            price=category.price
        )