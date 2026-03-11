# ==============================================================================
# REPOSITÓRIO DE VEÍCULOS
# ==============================================================================
from typing import List, Optional

from modules.fuel.domain.entities import  FuelRequest, Vehicle
from modules.fuel.domain.repositories import  FuelRequestRepository, VehicleRepository
from modules.fuel.domain.value_objects import FuelAmount, FuelRequestStatus, FuelType
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel
from shared.exceptions.custom_exceptions import ConflictException


class DjangoVehicleRepository(VehicleRepository):
    def _to_entity(self, model: VehicleModel) -> Vehicle:
        return Vehicle(
            id=model.id,
            license_plate=model.license_plate,
            model=model.model,
            tank_capacity=model.tank_capacity,
            fuel_type=FuelType(model.fuel_type),
            version=model.version  
        )

    def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        try:
            model = VehicleModel.objects.get(id=vehicle_id)
            return self._to_entity(model)
        except VehicleModel.DoesNotExist:
            return None

    def find_by_license_plate(self, plate: str) -> Optional[Vehicle]:
        try:
            model = VehicleModel.objects.get(license_plate=plate.upper())
            return self._to_entity(model)
        except VehicleModel.DoesNotExist:
            return None

    def list_all(self, filters: dict = None) -> List[Vehicle]:
        queryset = VehicleModel.objects.all().order_by('license_plate')
        if filters:
            queryset = queryset.filter(**filters)
        return [self._to_entity(model) for model in queryset]

    def save(self, vehicle: Vehicle, old_version: int) -> Vehicle:
        if vehicle.id is None:
            model = VehicleModel.objects.create(
                license_plate=vehicle.license_plate,
                model=vehicle.model,
                tank_capacity=vehicle.tank_capacity,
                fuel_type=vehicle.fuel_type.value,
                version=vehicle.version
            )
            vehicle.id = model.id
            return vehicle

        updated_count = VehicleModel.objects.filter(
            id=vehicle.id, 
            version=old_version
        ).update(
            license_plate=vehicle.license_plate,
            model=vehicle.model,
            tank_capacity=vehicle.tank_capacity,
            fuel_type=vehicle.fuel_type.value,
            version=vehicle.version
        )

        if updated_count == 0:
            raise ConflictException(
                f"Falha de concorrência: O veículo {vehicle.license_plate} já foi atualizado."
            )
        return vehicle


# ==============================================================================
# REPOSITÓRIO DE REQUISIÇÕES (V1 - Individual)
# ==============================================================================
class DjangoFuelRequestRepository(FuelRequestRepository):
    def _to_entity(self, model: FuelRequestModel) -> FuelRequest:
        vehicle = Vehicle(
            id=model.vehicle.id,
            license_plate=model.vehicle.license_plate,
            model=model.vehicle.model,
            tank_capacity=model.vehicle.tank_capacity,
            fuel_type=FuelType(model.vehicle.fuel_type)
        )
        return FuelRequest(
            id=model.id,
            vehicle=vehicle,
            requester_id=model.requester_id,
            amount=FuelAmount(model.liters),
            status=FuelRequestStatus(model.status),
            created_at=model.created_at,
            approved_at=model.approved_at,
            approved_by_id=model.approved_by_id,
            rejected_at=model.rejected_at,
            rejected_by_id=model.rejected_by_id,
            cancelled_at=model.cancelled_at,
            fueled_at=model.fueled_at,
            fueled_by_id=model.fueled_by_id
        )

    def save(self, request: FuelRequest) -> FuelRequest:
        model, _ = FuelRequestModel.objects.update_or_create(
            id=request.id,
            defaults={
                "vehicle_id": request.vehicle.id,
                "requester_id": request.requester_id,
                "liters": request.amount.liters,
                "status": request.status.value,
                "approved_by_id": request.approved_by_id,
                "approved_at": request.approved_at,
                "rejected_by_id": request.rejected_by_id,
                "rejected_at": request.rejected_at,
                "cancelled_at": request.cancelled_at,
                "fueled_by_id": request.fueled_by_id,
                "fueled_at": request.fueled_at,
            }
        )
        request.id = model.id
        return request

    def find_by_id(self, request_id: int) -> Optional[FuelRequest]:
        try:
            model = FuelRequestModel.objects.select_related('vehicle').get(id=request_id)
            return self._to_entity(model)
        except FuelRequestModel.DoesNotExist:
            return None

    def list_all(self, filters: dict = None) -> List[FuelRequest]:
        queryset = FuelRequestModel.objects.select_related('vehicle').all().order_by('-created_at')
        if filters:
            queryset = queryset.filter(**filters)
        return [self._to_entity(model) for model in queryset]

