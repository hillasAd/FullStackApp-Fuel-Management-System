from django.utils import timezone
from django.db import transaction

from modules.fuel.domain.exceptions import InvalidFuelStateTransition
from modules.fuelv2.domain.repositories import BulkFuelRepository
from modules.fuelv2.domain.value_objects import BulkItemStatus

class ProcessBulkItemUseCase:
    def __init__(self, bulk_repo: BulkFuelRepository, event_dispatcher):
        self.bulk_repo = bulk_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, dto) -> any:
        """
        Processa uma ação (APPROVE, REJECT, CANCEL, FUELED) num item específico.
        """
        with transaction.atomic():
            # 1. Recuperar o Agregado Completo (Header + Items)
            bulk = self.bulk_repo.find_header_by_id(dto.bulk_id)
            if not bulk:
                raise ValueError(f"Lote {dto.bulk_id} não encontrado.")

            # 2. Localizar o Item dentro do Agregado
            item = next((i for i in bulk.items if i.id == dto.item_id), None)
            if not item:
                raise ValueError(f"Viatura ID {dto.item_id} não pertence a este lote.")

            # 3. Delegar a Ação para a Entidade (Regras de Estado)
            action_upper = dto.action.upper()
            
            if action_upper == 'APPROVED':
                item.approve(dto.admin_id)
            
            elif action_upper == 'REJECTED':
                item.reject(dto.admin_id, dto.reason)
            
            elif action_upper == 'CANCELLED':
                item.status = BulkItemStatus.CANCELLED
            
            elif action_upper == 'FUELED':
                if item.status != BulkItemStatus.APPROVED:
                    raise InvalidFuelStateTransition("Apenas itens aprovados podem ser abastecidos.")
                item.status = BulkItemStatus.FUELED
                item.processed_at = timezone.now()
            
            else:
                raise InvalidFuelStateTransition(f"Ação {dto.action} desconhecida.")

            # 4. Sincronização Automática do Pai
            bulk.sync_status()

            # 5. Persistência do Agregado com Controle de Concorrência
            self.bulk_repo.save_item(item)
            
            # FIX: Passar dto.version para garantir Optimistic Locking
            self.bulk_repo.update_header_status(
                bulk_id=bulk.id, 
                new_status=bulk.status, 
                old_version=dto.version
            )

        # 6. Notificação de Evento
        self.event_dispatcher.dispatch(f"fuelv2.item_{dto.action.lower()}_2", {
            "bulk_id": bulk.id,
            "item_id": item.id,
            "new_bulk_status": bulk.status.value
        })

        return item
