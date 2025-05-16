from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository


class InscriptionRemover:
    def __init__(self, inscription_repository: InscriptionRepository):
        self.inscription_repo = inscription_repository

    def execute(self, inscription_id: int) -> str:
        # 1. Buscar inscripción por ID
        inscription = self.inscription_repo.find_by_id(inscription_id)
        if not inscription:
            raise ValueError("Inscripción no encontrada")

        # 2. Verificar si está confirmada
        if inscription.is_confirmed():
            return "No se puede eliminar una inscripción confirmada."

        # 3. Eliminar inscripción
        self.inscription_repo.delete(inscription)

        return "Inscripción eliminada correctamente."
