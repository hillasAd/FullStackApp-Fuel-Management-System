from modules.fuel.domain.services import UserProviderPort
from ....domain.repositories import FuelRequestRepository
from ....domain.events import FuelEvents
from shared.events.dispatcher import EventDispatcher
from shared.exceptions.custom_exceptions import NotFoundException

class ApproveFuelUseCase:
    def __init__(
        self, 
        fuel_repo: FuelRequestRepository, 
        event_dispatcher: EventDispatcher,
        user_provider: UserProviderPort
    ):
        self.fuel_repo = fuel_repo
        self.event_dispatcher = event_dispatcher
        self.user_provider = user_provider

    def execute(self, request_id: int, admin_id: int):
        fuel_request = self.fuel_repo.find_by_id(request_id)
        if not fuel_request:
            raise NotFoundException("Pedido não encontrado.")

        fuel_request.approve(admin_id=admin_id)
        self.fuel_repo.save(fuel_request)

        user_info = self.user_provider.get_user_contact_info(fuel_request.requester_id)

        self.event_dispatcher.dispatch(
            event_name=FuelEvents.REQUEST_APPROVED,
            payload={
                "request_id": fuel_request.id,
                "admin_id": admin_id,
                "status": fuel_request.status.value,
                **user_info
            }
        )
        return fuel_request
