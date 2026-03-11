from typing import Optional

from modules.fuelv2.domain.entities import BulkFuelRequest
from modules.fuelv2.domain.repositories import BulkFuelRepository


class GetBulkDetailUseCase:
    def __init__(self, bulk_repo: BulkFuelRepository):
        self.bulk_repo = bulk_repo

    def execute(self, bulk_id: int) -> Optional[BulkFuelRequest]:
        """
        Recupera o Agregado Bulk completo com todos os itens e veículos.
        """
        # 1. Busca no Repositório
        bulk = self.bulk_repo.find_header_by_id(bulk_id)
        
        if not bulk:
            return None
            
        # 2. Sincroniza o status antes de entregar à View
        # Garante que se todos os itens foram cancelados, o status do lote seja CANCELLED
        bulk.sync_status()
        
        return bulk
