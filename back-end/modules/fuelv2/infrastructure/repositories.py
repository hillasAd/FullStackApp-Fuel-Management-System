from typing import Optional

from modules.fuelv2.domain.repositories import BulkFuelRepository
from shared.exceptions.custom_exceptions import ConflictException
from .models import BulkFuelRequestModel, BulkFuelRequestItemModel
from ..domain.entities import BulkFuelRequest, BulkFuelRequestItem, Vehicle
from ..domain.value_objects import BulkItemStatus, BulkStatus
from modules.fuel.domain.value_objects import FuelAmount, FuelType

class DjangoBulkFuelRepository(BulkFuelRepository):

    def _to_entity(self, model: BulkFuelRequestModel) -> BulkFuelRequest:
        """Converte Model Django -> Entidade de Domínio com Itens Reais"""
        items = []

        for item_model in model.items.all():
            vehicle = Vehicle(
                id=item_model.vehicle.id,
                license_plate=item_model.vehicle.license_plate,
                model=item_model.vehicle.model,
                tank_capacity=item_model.vehicle.tank_capacity,
                fuel_type=FuelType(item_model.vehicle.fuel_type)
            )
            items.append(BulkFuelRequestItem(
                id=item_model.id,
                vehicle=vehicle,
                amount=FuelAmount(item_model.liters),
                status=BulkItemStatus(item_model.status),
                processed_at=item_model.processed_at,
                processed_by_id=item_model.processed_by_id,
                rejection_reason=item_model.rejection_reason
            ))

        return BulkFuelRequest(
            id=model.id,
            requester_id=model.requester_id,
            description=model.description,
            items=items,
            status=BulkStatus(model.status),
            cancellation_reason=model.cancellation_reason,
            created_at=model.created_at,
            version=model.version
        )

    def save_bulk(self, bulk_request: BulkFuelRequest) -> BulkFuelRequest:
        """Persiste o Agregado Completo (Master/Detail)"""
        header_model = BulkFuelRequestModel.objects.create(
            requester_id=bulk_request.requester_id,
            description=bulk_request.description,
            status=bulk_request.status.value,
            version=bulk_request.version
        )
        
        for item in bulk_request.items:
            item_model = BulkFuelRequestItemModel.objects.create(
                parent_request=header_model,
                vehicle_id=item.vehicle.id,
                liters=item.amount.liters,
                status=item.status.value
            )
            item.id = item_model.id
            
        bulk_request.id = header_model.id
        return bulk_request

    def find_header_by_id(self, header_id: int) -> Optional[BulkFuelRequest]:
        try:

            model = BulkFuelRequestModel.objects.prefetch_related(
                'items__vehicle'
            ).get(id=header_id)
            return self._to_entity(model)
        except BulkFuelRequestModel.DoesNotExist:
            return None

    def find_all_headers(self, filters: dict = None) -> list[BulkFuelRequest]:
        queryset = BulkFuelRequestModel.objects.prefetch_related('items__vehicle').all()
        if filters:
            queryset = queryset.filter(**filters)
        return [self._to_entity(m) for m in queryset]

    def find_item_by_id(self, item_id: int) -> Optional[BulkFuelRequestItem]:
        try:
            item_model = BulkFuelRequestItemModel.objects.select_related('vehicle').get(id=item_id)

            vehicle = Vehicle(
                id=item_model.vehicle.id,
                license_plate=item_model.vehicle.license_plate,
                model=item_model.vehicle.model,
                tank_capacity=item_model.vehicle.tank_capacity,
                fuel_type=FuelType(item_model.vehicle.fuel_type)
            )
            return BulkFuelRequestItem(
                id=item_model.id,
                vehicle=vehicle,
                amount=FuelAmount(item_model.liters),
                status=BulkItemStatus(item_model.status)
            )
        except BulkFuelRequestItemModel.DoesNotExist:
            return None

    def save_item(self, item: BulkFuelRequestItem) -> None:
        """Persiste apenas as alterações de um item (Aprovação/Rejeição/Fuel)"""
        BulkFuelRequestItemModel.objects.filter(id=item.id).update(
            status=item.status.value,
            processed_by_id=item.processed_by_id,
            processed_at=item.processed_at,
            rejection_reason=item.rejection_reason
        )
        

    def update_header_status(self, bulk_id: int, new_status: BulkStatus, old_version: int, cancellation_reason: str = None) -> None:
        """Executa o Optimistic Locking atualizando status e razão de cancelamento"""
        updated_count = BulkFuelRequestModel.objects.filter(
            id=bulk_id, 
            version=old_version
        ).update(
            status=new_status.value,
            cancellation_reason=cancellation_reason,
            version=old_version + 1
        )

        if updated_count == 0:
            raise ConflictException(f"O lote {bulk_id} foi alterado por outro usuário.")
