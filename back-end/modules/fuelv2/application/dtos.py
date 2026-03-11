from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FuelItemDTO:
    """Representa uma linha (viatura) dentro do lote vindo da API"""
    vehicle_id: int
    liters: float

@dataclass
class BulkFuelRequestDTO:
    """Representa a requisição completa de criação de lote"""
    requester_id: int
    description: str
    items: List[FuelItemDTO]

@dataclass
class ProcessItemDTO:
    """Representa a ação de aprovação/rejeição de um item específico"""
    bulk_id: int
    item_id: int
    admin_id: int
    action: str  # 'APPROVE', 'REJECT', 'CANCEL', 'COMPLETED'
    version: int
    reason: Optional[str] = None
   
