from modules.dashboard.domain.repositories import IDashboardRepository


class GetDashboardSummaryUseCase:
    def __init__(self, repository: IDashboardRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_aggregated_stats()
