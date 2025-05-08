from typing import Optional

from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.vouchers.domain.VoucherRepository import VoucherRepository


class InscriptionUpdater:
    def __init__(
        self,
        inscription_repository: InscriptionRepository,
        area_repository: AreaRepository,
        category_repository: CategoryRepository,
        voucher_repository: VoucherRepository
    ):
        self.inscription_repo = inscription_repository
        self.area_repo = area_repository
        self.category_repo = category_repository
        self.voucher_repo = voucher_repository

    def execute(
        self,
        inscription_id: int,
        new_area_id: int,
        new_category_id: int,
    ) -> str:
        # 1. Buscar inscripción original
        inscription = self.inscription_repo.find_by_id(inscription_id)
        if not inscription:
            raise ValueError("Inscription not found")

        # 2. Verificar si la inscripción ya fue confirmada
        if inscription.is_confirmed():
            return "La inscripción ya fue confirmada y no se puede editar."

        # 3. Validar existencia de nuevos valores
        if not self.area_repo.find_by_id(new_area_id):
            raise ValueError("Area not found")

        if not self.category_repo.find_by_id(new_category_id):
            raise ValueError("Category not found")

        # 4. Buscar si ya existe una inscripción con esos valores para el mismo estudiante y evento
        inscription_duplicate = self.inscription_repo.find_by_ids(
            student_id=inscription.student_id,
            event_id=inscription.event_id,
            area_id=new_area_id,
            category_id=new_category_id
        )

        if inscription_duplicate:
            return "Ya existe una inscripción con esos valores para el estudiante."

        # 5. Actualizar inscripción
        inscription.area_id = new_area_id
        inscription.category_id = new_category_id
        inscription.remove_voucher()  # eliminar voucher si existe
        inscription.update_status()   # marcar como pendiente

        # 6. Guardar cambios
        self.inscription_repo.update(inscription)

        return "Se editó la inscripción correctamente."
