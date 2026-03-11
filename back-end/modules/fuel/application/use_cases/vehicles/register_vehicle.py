from ....domain.entities import Vehicle
from ....domain.repositories import VehicleRepository
from ....domain.value_objects import FuelType
from ....domain.exceptions import VehicleAlreadyRegistered
from ...dtos import VehicleDTO

class RegisterVehicleUseCase:
    def __init__(self, vehicle_repo: VehicleRepository):
        self.vehicle_repo = vehicle_repo

    def execute(self, dto: VehicleDTO) -> Vehicle:
        # 1. Verificar se a viatura já existe pela placa
        existing_vehicle = self.vehicle_repo.find_by_license_plate(dto.license_plate)
        if existing_vehicle:
            raise VehicleAlreadyRegistered()

        # 2. Criar a Entidade de Domínio
        new_vehicle = Vehicle(
            id=None,
            license_plate=dto.license_plate,
            model=dto.model,
            tank_capacity=dto.tank_capacity,
            fuel_type=FuelType(dto.fuel_type.upper())
        )

        # 3. Persistir via Repositório
        return self.vehicle_repo.save(new_vehicle, new_vehicle.version)
