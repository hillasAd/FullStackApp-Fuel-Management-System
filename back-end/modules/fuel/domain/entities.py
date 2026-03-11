from django.utils import timezone
from typing import Optional
from .value_objects import FuelRequestStatus, FuelAmount, FuelType
from .exceptions import InvalidFuelStateTransition, TankCapacityExceeded

class Vehicle:
    def __init__(self, id: Optional[int], license_plate: str, model: str, tank_capacity: float, fuel_type: FuelType, version: int = 1):
        self.id = id
        self.license_plate = license_plate.upper()
        self.model = model
        self.tank_capacity = tank_capacity
        self.fuel_type = fuel_type
        self.version = version
        
    def update_info(self, license_plate, model, tank_capacity, fuel_type):
        self.license_plate = license_plate.upper()
        self.model = model
        self.tank_capacity = tank_capacity
        self.fuel_type = fuel_type
        self.version += 1


class FuelRequest:
    def __init__(self, id: Optional[int], vehicle: Vehicle, requester_id: int, amount: FuelAmount, **kwargs):
        self.id = id
        self.vehicle = vehicle
        self.requester_id = requester_id
        self.amount = amount
        self.status = kwargs.get('status', FuelRequestStatus.PENDING)
        
        self.created_at = kwargs.get('created_at', timezone.now())
        self.approved_at = kwargs.get('approved_at')
        self.approved_by_id = kwargs.get('approved_by_id')
        self.rejected_at = kwargs.get('rejected_at')
        self.rejected_by_id = kwargs.get('rejected_by_id')
        self.cancelled_at = kwargs.get('cancelled_at')
        self.fueled_at = kwargs.get('fueled_at')
        self.fueled_by_id = kwargs.get('fueled_by_id')

        if self.amount.liters > self.vehicle.tank_capacity * 1.10:
            raise TankCapacityExceeded()

    def approve(self, admin_id: int):
        if self.status != FuelRequestStatus.PENDING:
            raise InvalidFuelStateTransition()
        self.status = FuelRequestStatus.APPROVED
        self.approved_by_id = admin_id
        self.approved_at = timezone.now()

    def reject(self, admin_id: int):
        if self.status != FuelRequestStatus.PENDING:
            raise InvalidFuelStateTransition()
        self.status = FuelRequestStatus.REJECTED
        self.rejected_by_id = admin_id
        self.rejected_at = timezone.now()

    def cancel(self):
        if self.status not in [FuelRequestStatus.PENDING, FuelRequestStatus.APPROVED, FuelRequestStatus.CANCELLED]:
            raise InvalidFuelStateTransition()
        self.status = FuelRequestStatus.CANCELLED
        self.cancelled_at = timezone.now()

    def mark_as_fueled(self, operator_id: int):
        if self.status != FuelRequestStatus.APPROVED:
            raise InvalidFuelStateTransition()
        self.status = FuelRequestStatus.FUELED
        self.fueled_by_id = operator_id
        self.fueled_at = timezone.now()

