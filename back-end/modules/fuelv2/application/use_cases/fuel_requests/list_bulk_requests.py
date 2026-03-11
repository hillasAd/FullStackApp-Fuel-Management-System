from typing import List, Optional

from modules.fuelv2.domain.entities import BulkFuelRequest
from modules.fuelv2.domain.repositories import BulkFuelRepository


class ListBulkRequestsUseCase:
    def __init__(self, bulk_repo: BulkFuelRepository):
        self.bulk_repo = bulk_repo

    def execute(self, filters: Optional[dict] = None) -> List[BulkFuelRequest]:
        """
        Retorna a lista de Agregados Bulk (Header + Items).
        O repositório já deve usar prefetch_related para evitar N+1 queries.
        """
        # 1. Recuperar do Repositório (Já convertido para Entidade)
        bulk_requests = self.bulk_repo.find_all_headers(filters=filters)
        
        # 2. Garantir Consistência de Domínio
        # Percorremos a lista para rodar a lógica de sincronismo da V2
        for bulk in bulk_requests:
            bulk.sync_status()
            
        return bulk_requests
