from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository


class StatisticsService:
    def __init__(self, stats_repo: InscriptionRepository):
        self.stats_repo = stats_repo


    def get_event_statistics(self, event_id: int) -> dict:
        """Obtiene todas las estadísticas para un evento específico"""
        return {
            "students_by_category": self.stats_repo.get_students_by_category(event_id),
            "students_by_area": self.stats_repo.get_students_by_area(event_id),
            "inscriptions_timeline": self.stats_repo.get_inscriptions_timeline(event_id),
            "completion_ratio": {
                "completed": self.stats_repo.get_completion_ratio(event_id)[0],
                "incomplete": self.stats_repo.get_completion_ratio(event_id)[1]
            },
            "payment_status_distribution": self.stats_repo.get_payment_status_distribution(event_id),
            "inscription_funnel": self.stats_repo.get_inscription_funnel(event_id),
            "stacked_bar_data": self.stats_repo.get_stacked_bar_data(event_id)
        }