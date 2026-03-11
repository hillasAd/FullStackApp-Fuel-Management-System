from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class VehicleDTO:
    license_plate: str
    model: str
    tank_capacity: float
    fuel_type: str
    id: Optional[int] = None
    version: Optional[int] = 1

@dataclass(frozen=True)
class FuelRequestDTO:
    vehicle_id: int
    requester_id: int
    liters: float
    status: Optional[str] = "PENDING"
