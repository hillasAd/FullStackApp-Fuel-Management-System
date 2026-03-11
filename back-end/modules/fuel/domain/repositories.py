import abc
from typing import List, Optional
from .entities import Vehicle, FuelRequest

class VehicleRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, vehicle: Vehicle, old_version: any) -> Vehicle: pass

    @abc.abstractmethod
    def find_by_license_plate(self, plate: str) -> Optional[Vehicle]: pass

    @abc.abstractmethod
    def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]: pass
    
    @abc.abstractmethod
    def list_all(self, filters: dict = None) -> List[Vehicle]: pass


class FuelRequestRepository(abc.ABC):
    """Focado na Versão 1: Operações simples de requisição individual"""
    @abc.abstractmethod
    def save(self, request: FuelRequest) -> FuelRequest: pass

    @abc.abstractmethod
    def find_by_id(self, request_id: int) -> Optional[FuelRequest]: pass
    
    @abc.abstractmethod
    def list_all(self, filters: dict = None) -> List[FuelRequest]: pass


