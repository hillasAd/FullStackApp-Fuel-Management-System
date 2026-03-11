from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from django.utils import timezone

from .value_objects import BulkItemStatus, BulkStatus
from modules.fuel.domain.entities import Vehicle
from modules.fuel.domain.value_objects import FuelAmount
from modules.fuel.domain.exceptions import InvalidFuelStateTransition, TankCapacityExceeded

class BulkFuelRequestItem:
    def __init__(self, id: Optional[int], vehicle: Vehicle, amount: FuelAmount, **kwargs):
        self.id = id
        self.vehicle = vehicle
        self.amount = amount
        self.status = kwargs.get('status', BulkItemStatus.PENDING)
        self.processed_at = kwargs.get('processed_at')
        self.processed_by_id = kwargs.get('processed_by_id')
        self.rejection_reason = kwargs.get('rejection_reason')

        if self.amount.liters > self.vehicle.tank_capacity * 1.10:
            raise TankCapacityExceeded()

    def approve(self, admin_id: int):
        if str(self.status.value) != "PENDING":
            raise InvalidFuelStateTransition(f"Apenas itens PENDING podem ser aprovados.")
        self.status = BulkItemStatus.APPROVED
        self.processed_by_id = admin_id
        self.processed_at = timezone.now()

    def reject(self, admin_id: int, reason: str):
        if str(self.status.value) != "PENDING":
            raise InvalidFuelStateTransition(f"Apenas itens PENDING podem ser rejeitados.")
        if not reason:
            raise ValueError("Razão de rejeição obrigatória.")
        self.status = BulkItemStatus.REJECTED
        self.processed_by_id = admin_id
        self.processed_at = timezone.now()
        self.rejection_reason = reason

@dataclass
class BulkFuelRequest:
    id: Optional[int]
    requester_id: int
    description: str
    items: List[BulkFuelRequestItem] = field(default_factory=list)
    status: BulkStatus = BulkStatus.PENDING
    cancellation_reason: Optional[str] = None
    created_at: datetime = field(default_factory=timezone.now)
    version: int = 1 

    def add_item(self, vehicle: Vehicle, amount: FuelAmount):
        if self.status != BulkStatus.PENDING:
            raise InvalidFuelStateTransition("Não é possível adicionar itens a um lote já processado.")
        
        item = BulkFuelRequestItem(id=None, vehicle=vehicle, amount=amount)
        self.items.append(item)

    def cancel_master(self, reason: str):
        if self.status == BulkStatus.COMPLETED:
            raise InvalidFuelStateTransition("Lote já concluído não pode ser cancelado.")
        if not reason:
            raise ValueError("Razão de cancelamento é obrigatória.")
            
        self.status = BulkStatus.CANCELLED
        self.cancellation_reason = reason
        for item in self.items:
            if str(item.status.value) == "PENDING":
                item.status = BulkItemStatus.CANCELLED

    def sync_status(self):
        """Sincroniza o status do PAI baseado nos FILHOS (Itens)"""
        if self.status in [BulkStatus.CANCELLED, BulkStatus.COMPLETED]:
            return
        
        item_statuses = [i.status.value for i in self.items]
        if not item_statuses:
            return
        
        # Conjunto de valores únicos para facilitar a lógica de decisão
        unique_statuses = set(item_statuses)
        
        # 1. Se todos forem REJECTED, o pai também será
        if unique_statuses == {"REJECTED"}:
            self.status = BulkStatus.CANCELLED
            return
                 
        total = len(self.items)
        if total == 0: return

        # Contabiliza estados terminais
        finished_count = sum(1 for i in self.items if str(i.status.value) in ["FUELED", "REJECTED", "REJECTED"])
        # Contabiliza qualquer alteração
        touched_count = sum(1 for i in self.items if str(i.status.value) != "PENDING")

        if finished_count == total:
            self.status = BulkStatus.COMPLETED
        elif touched_count > 0:
            self.status = BulkStatus.PROCESSED
