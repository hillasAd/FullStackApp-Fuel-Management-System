from django.db import transaction


# Repositório de veículos do módulo original (V1)
from modules.fuel.domain.repositories import VehicleRepository
from modules.fuel.domain.value_objects import FuelAmount
from modules.fuelv2.domain.entities import BulkFuelRequest
from modules.fuelv2.domain.repositories import BulkFuelRepository

class CreateBulkRequestUseCase:
    def __init__(
        self, 
        bulk_repo: BulkFuelRepository, 
        vehicle_repo: VehicleRepository, 
        event_dispatcher
    ):
        self.bulk_repo = bulk_repo
        self.vehicle_repo = vehicle_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, dto) -> BulkFuelRequest:
        """
        Cria um lote de combustível (Bulk).
        O DTO garante que dto.items é uma List[FuelItemDTO].
        """
        # 1. Validação de Regra de Negócio Inicial
        if not dto.items:
            raise ValueError("O lote deve conter pelo menos uma viatura.")

        # 2. Instanciar o Agregado Root (Entidade)
        bulk_request = BulkFuelRequest(
            id=None,
            requester_id=dto.requester_id,
            description=dto.description,
            items=[]
        )

        # 3. Construção do Agregado com Validação de Viatura e Capacidade
        for item_dto in dto.items:
            
            vehicle = self.vehicle_repo.find_by_id(item_dto.vehicle_id)
            if not vehicle:
                raise ValueError(f"Viatura ID {item_dto.vehicle_id} não encontrada.")
            
            bulk_request.add_item(
                vehicle=vehicle,
                amount=FuelAmount(liters=item_dto.liters)
            )

        # 4. Persistência Atómica do Agregado Completo
        with transaction.atomic():
            # O repositório recebe a ENTIDADE e trata de salvar Master/Detail
            saved_bulk = self.bulk_repo.save_bulk(bulk_request)

        # 5. Notificação de Evento (Clean Architecture)
        self.event_dispatcher.dispatch("fuel.bulk_request_created_2", {
            "bulk_id": saved_bulk.id,
            "requester_id": saved_bulk.requester_id,
            "total_items": len(saved_bulk.items)
        })
        
        return saved_bulk
