import structlog
from ....domain.entities import FuelRequest
from ....domain.repositories import FuelRequestRepository, VehicleRepository
from ....domain.value_objects import FuelAmount
from ....domain.events import FuelEvents
from ....application.dtos import FuelRequestDTO
from shared.events.dispatcher import EventDispatcher
from shared.exceptions.custom_exceptions import NotFoundException

logger = structlog.get_logger(__name__)

class RequestFuelUseCase:
    def __init__(
        self, 
        fuel_repo: FuelRequestRepository, 
        vehicle_repo: VehicleRepository,
        event_dispatcher: EventDispatcher
    ):
        self.fuel_repo = fuel_repo
        self.vehicle_repo = vehicle_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, dto: FuelRequestDTO) -> FuelRequest:
        # 1. Buscar a viatura (para validar capacidade do tanque)
        vehicle = self.vehicle_repo.find_by_id(dto.vehicle_id)
        if not vehicle:
            raise NotFoundException("Viatura não encontrada.")

        # 2. Criar a Entidade
        fuel_request = FuelRequest(
            id=None,
            vehicle=vehicle,
            requester_id=dto.requester_id,
            amount=FuelAmount(dto.liters)
        )

        # 3. Persistir
        saved_request = self.fuel_repo.save(fuel_request)

        # 4. Disparar Evento para Notificações (Manager deve ouvir isso)
        self.event_dispatcher.dispatch(
            event_name=FuelEvents.REQUEST_CREATED,
            payload={
                "request_id": saved_request.id,
                "vehicle_plate": vehicle.license_plate,
                "liters": saved_request.amount.liters,
                "requester_id": saved_request.requester_id
            }
        )

        logger.info("fuel_request_created", request_id=saved_request.id, vehicle=vehicle.license_plate)
        return saved_request
