from shared.exceptions.custom_exceptions import NotFoundException


class FuelingCompletedUseCase:
    def __init__(self, fuel_repo, event_dispatcher):
        self.fuel_repo = fuel_repo
        self.event_dispatcher = event_dispatcher
        

    def execute(self, request_id: int, operator_id: int):
        fuel_request = self.fuel_repo.find_by_id(request_id)
        if not fuel_request: raise NotFoundException("Pedido não encontrado.")

        # Transição: APPROVED -> FUELED
        fuel_request.mark_as_fueled(operator_id=operator_id)
        self.fuel_repo.save(fuel_request)

        self.event_dispatcher.dispatch("fuel.fueling_completed", {
            "request_id": fuel_request.id, "requester_id": fuel_request.requester_id
        })
        return fuel_request