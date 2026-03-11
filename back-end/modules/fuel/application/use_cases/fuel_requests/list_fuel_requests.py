from ....domain.repositories import FuelRequestRepository

class ListFuelRequestsUseCase:
    def __init__(self, fuel_repo: FuelRequestRepository):
        self.fuel_repo = fuel_repo

    def execute(self, filters: dict = None):
        return self.fuel_repo.list_all(filters)
