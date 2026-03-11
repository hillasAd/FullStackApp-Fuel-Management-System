from dataclasses import dataclass
from enum import Enum

from modules.fuel.domain.exceptions import InvalidFuelAmountException

class FuelType(Enum):
    DIESEL = "DIESEL"
    GASOLINE = "GASOLINE"

class FuelRequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    FUELED = "FUELED"

@dataclass(frozen=True)
class FuelAmount:
    liters: float

    def __post_init__(self):
        if (self.liters <= 0) or (self.liters>=200):
            raise InvalidFuelAmountException()
