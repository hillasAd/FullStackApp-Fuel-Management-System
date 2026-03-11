from ....domain.repositories import VehicleRepository
from shared.exceptions.custom_exceptions import NotFoundException

class GetVehicleUseCase:
    def __init__(self, vehicle_repo: VehicleRepository):
        self.vehicle_repo = vehicle_repo

    def execute_list(self) -> list:
        # Retorna todas as viaturas registadas
        return self.vehicle_repo.list_all()

    def execute_detail(self, vehicle_id: int):
        # Retorna uma viatura específica ou explode 404
        vehicle = self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise NotFoundException("Viatura não encontrada no sistema.")
        return vehicle
