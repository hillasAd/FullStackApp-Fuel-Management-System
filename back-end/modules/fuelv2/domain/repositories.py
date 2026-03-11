import abc
from typing import Optional

from modules.fuelv2.domain.entities import BulkFuelRequest, BulkFuelRequestItem, BulkStatus


class BulkFuelRepository(abc.ABC):

    @abc.abstractmethod
    def save_bulk(self, bulk_request: BulkFuelRequest) -> BulkFuelRequest:
        """Persiste o agregado completo (Header + Itens) pela primeira vez"""
        pass

    @abc.abstractmethod
    def find_header_by_id(self, header_id: int) -> Optional[BulkFuelRequest]:
        """Busca o lote completo (Agregado) para detalhe ou processamento"""
        pass

    @abc.abstractmethod
    def find_all_headers(self, filters: dict = None) -> list[BulkFuelRequest]:
        """Lista todos os lotes (Agregados) convertidos para domínio"""
        pass

    @abc.abstractmethod
    def find_item_by_id(self, item_id: int) -> Optional[BulkFuelRequestItem]:
        """Busca um item específico para processamento individual (Requisito 4)"""
        pass

    @abc.abstractmethod
    def save_item(self, item: BulkFuelRequestItem) -> None:
        """Persiste a mudança de estado (Aprovar/Rejeitar) de um item específico"""
        pass

    @abc.abstractmethod
    def update_header_status(self, bulk_id: int, new_status: BulkStatus, version: int) -> None:
        """Atualiza apenas o status do cabeçalho (ex: após sync_status)"""
        pass
