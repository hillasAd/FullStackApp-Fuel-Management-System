from ....domain.entities import Vehicle
from ....domain.repositories import VehicleRepository
from ....domain.value_objects import FuelType
from ....domain.exceptions import VehicleAlreadyRegistered
from shared.exceptions.custom_exceptions import ConflictException, NotFoundException

from ...dtos import VehicleDTO

class UpdateVehicleUseCase:
    def __init__(self, vehicle_repo: VehicleRepository):
        self.vehicle_repo = vehicle_repo

    def execute(self, vehicle_id: int, dto: VehicleDTO) -> Vehicle:
        # 1. Verificar se a viatura existe
        vehicle = self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise NotFoundException("Viatura não encontrada.")

        # 2. Se a placa mudou, verificar se a nova placa já está em uso por OUTRO id
        existing = self.vehicle_repo.find_by_license_plate(dto.license_plate)
        if existing and existing.id != vehicle_id:
            raise VehicleAlreadyRegistered("Esta nova placa já está registada em outra viatura.")

        # Validação de Concorrência (Pessimistic/Optimistic Locking)
        if dto.version is not None and vehicle.version != dto.version:
            raise ConflictException("O veículo foi alterado por outro utilizador.")
    
    
         # Atualiza e incrementa versão internamente
        vehicle.update_info(dto.license_plate, dto.model, dto.tank_capacity, FuelType(dto.fuel_type.upper()))

        # O segredo está no SAVE
        return self.vehicle_repo.save(vehicle, old_version=dto.version)
    
        