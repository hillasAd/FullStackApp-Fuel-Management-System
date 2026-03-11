from django.utils import timezone
from django.db import transaction
from modules.fuelv2.domain.value_objects import BulkItemStatus, BulkStatus

class ProcessBulkActionUseCase:
    def __init__(self, bulk_repo, event_dispatcher):
        self.bulk_repo = bulk_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, dto):
        with transaction.atomic():
            # 1. Recupera o agregado completo (Pai + Itens)
            bulk = self.bulk_repo.find_header_by_id(dto.bulk_id)
            if not bulk:
                raise ValueError(f"Lote {dto.bulk_id} não encontrado.")
            
            # 2. Trava de Segurança: Lote fechado é imutável
            current_status = str(bulk.status.value)
            if current_status in ['COMPLETED', 'CANCELLED']:
                raise ValueError(f"Operação negada: Lote já encerrado como {current_status}.")

            action = dto.action.upper()
            
            # 3. Processamento das Ações Globais
            if action == 'CANCELLED':
                bulk.cancel_master(dto.reason)
                
            elif action == 'APPROVED':
                for item in bulk.items:
                    if str(item.status.value) == "PENDING":
                        item.approve(dto.admin_id)
                bulk.sync_status()
                
            elif action == 'REJECTED':
                if not dto.reason:
                    raise ValueError("Justificativa obrigatória para rejeitar o lote.")
                for item in bulk.items:
                    if str(item.status.value) == "PENDING":
                        item.reject(dto.admin_id, dto.reason)
                bulk.sync_status()

            elif action == 'COMPLETED':
                # Forçamos a finalização de todos os itens e do cabeçalho
                for item in bulk.items:
                    if str(item.status.value) == "APPROVED":
                        item.status = BulkItemStatus.FUELED
                        item.processed_at = timezone.now()
                    elif str(item.status.value) == "PENDING":
                        item.status = BulkItemStatus.CANCELLED
                bulk.status = BulkStatus.COMPLETED
            
            else:
                raise ValueError(f"Ação global {action} desconhecida.")

            # 4. Persistência de Dados
            # Salva os itens um a um
            for item in bulk.items:
                self.bulk_repo.save_item(item)

            # Salva o Header (Pai) forçando o status atualizado e incrementando versão
            self.bulk_repo.update_header_status(
                bulk_id=bulk.id,
                new_status=bulk.status,
                old_version=dto.version,
                cancellation_reason=bulk.cancellation_reason 
            )
            
            bulk.version = dto.version + 1

        # 5. Disparo de Eventos
        self.event_dispatcher.dispatch(f"fuelv2.bulk_{action.lower()}", {
            "bulk_id": bulk.id,
            "status": bulk.status.value,
            "admin_id": dto.admin_id
        })

        return bulk
