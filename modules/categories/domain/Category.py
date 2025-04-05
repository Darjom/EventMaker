from typing import Optional

class Category:
    def __init__(
        self,
        category_id: Optional[int],
        area_id: int,
        category_name: str,
        description: Optional[str] = None,
        price: Optional[int] = None
    ):
        self.category_id = category_id
        self.area_id = area_id
        self.category_name = category_name
        self.description = description
        self.price = price
        # Validaciones de negocio
        if price is not None and price < 0:
            raise ValueError("El precio no puede ser negativo")

        if not category_name:
            raise ValueError("El nombre de la categoría es requerido")

    def __str__(self):
        return (
            f"Category(ID={self.category_id}, Name={self.category_name}, "
            f"Description={self.description}, Price={self.price})"
        )


