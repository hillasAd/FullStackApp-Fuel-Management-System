from modules.fuelv2.application.use_cases.fuel_requests.create_bulk_request import CreateBulkRequestUseCase
from modules.fuelv2.application.use_cases.fuel_requests.get_bulk_detail import GetBulkDetailUseCase
from modules.fuelv2.application.use_cases.fuel_requests.list_bulk_requests import ListBulkRequestsUseCase
from modules.fuelv2.application.use_cases.fuel_requests.process_bulk_global import ProcessBulkActionUseCase
from modules.fuelv2.application.use_cases.fuel_requests.process_bulk_item import ProcessBulkItemUseCase

from shared.events.django_dispatcher import DjangoLocalDispatcher
from modules.fuel.infrastructure.repositories import DjangoVehicleRepository
from .repositories import DjangoBulkFuelRepository

class BulkFuelUseCaseFactory:
    """
    Fábrica especializada para o Módulo Bulk (V2).
    Injeta Repositórios e Eventos nos Use Cases.
    """

    @staticmethod
    def _get_common_deps():
        """Helper para dependências padrão do módulo V2"""
        return {
            "bulk_repo": DjangoBulkFuelRepository(),
            "event_dispatcher": DjangoLocalDispatcher()
        }

    @staticmethod
    def create_bulk_request() -> CreateBulkRequestUseCase:
        """Criação de Lotes (Header + Itens)"""
        return CreateBulkRequestUseCase(
            vehicle_repo=DjangoVehicleRepository(),
            **BulkFuelUseCaseFactory._get_common_deps()
        )

    @staticmethod
    def create_process_bulk_item() -> ProcessBulkItemUseCase:
        """Aprovação, Rejeição e Finalização Individual"""
        return ProcessBulkItemUseCase(
            **BulkFuelUseCaseFactory._get_common_deps()
        )

    @staticmethod
    def create_process_bulk_action() -> ProcessBulkActionUseCase:
        """Aprovação, Rejeição e Cancelamento Global do Lote"""
        return ProcessBulkActionUseCase(
            **BulkFuelUseCaseFactory._get_common_deps()
        )

    @staticmethod
    def create_list_bulk_requests():
        """Listagem de Agregados V2"""
        return ListBulkRequestsUseCase(
            bulk_repo=DjangoBulkFuelRepository()
        )

    @staticmethod
    def create_get_bulk_detail():
        """Detalhe do Agregado V2"""
        return GetBulkDetailUseCase(
            bulk_repo=DjangoBulkFuelRepository()
        )
