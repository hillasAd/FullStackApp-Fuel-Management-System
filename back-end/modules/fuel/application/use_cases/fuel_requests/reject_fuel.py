from shared.exceptions.custom_exceptions import NotFoundException


class RejectFuelUseCase:
    def __init__(self, fuel_repo, event_dispatcher):
        self.fuel_repo = fuel_repo
        self.event_dispatcher = event_dispatcher

    def execute(self, request_id: int, admin_id: int):
        fuel_request = self.fuel_repo.find_by_id(request_id)
        if not fuel_request: raise NotFoundException("Pedido não encontrado.")

        fuel_request.reject(admin_id=admin_id)
        self.fuel_repo.save(fuel_request)
        
        self.event_dispatcher.dispatch("fuel.request_rejected", {
            "request_id": fuel_request.id, "requester_id": fuel_request.requester_id
        })
        return fuel_request