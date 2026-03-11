import structlog
from ....domain.repositories import FuelRequestRepository
from ....domain.events import FuelEvents
from shared.events.dispatcher import EventDispatcher
from shared.exceptions.custom_exceptions import NotFoundException, PermissionDeniedException

logger = structlog.get_logger(__name__)

class CancelFuelUseCase:
    def __init__(
        self, 
        fuel_repo: FuelRequestRepository, 
        event_dispatcher: EventDispatcher
    ):
        self.fuel_repo = fuel_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, request_id: int, user_id: int):
        # 1. Recuperar o pedido
        fuel_request = self.fuel_repo.find_by_id(request_id)
        if not fuel_request:
            raise NotFoundException("Pedido de combustível não encontrado.")

        # 2. Regra de Negócio: Apenas o dono do pedido pode cancelar
        if fuel_request.requester_id != user_id:
            raise PermissionDeniedException("Não tens permissão para cancelar este pedido.")

        # 3. Lógica de Domínio
        fuel_request.cancel()

        # 4. Persistir
        self.fuel_repo.save(fuel_request)

        # 5. Notificar via Evento
        self.event_dispatcher.dispatch(
            event_name=FuelEvents.REQUEST_CANCELLED,
            payload={
                "request_id": fuel_request.id,
                "requester_id": fuel_request.requester_id,
                "cancelled_at": fuel_request.cancelled_at
            }
        )

        logger.info("fuel_request_cancelled", request_id=fuel_request.id, user_id=user_id)
        return fuel_request
