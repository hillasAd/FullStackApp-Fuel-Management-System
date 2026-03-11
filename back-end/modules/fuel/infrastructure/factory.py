# infrastructure/factories.py

# --- COMPARTILHADO & INFRA ---
from shared.events.django_dispatcher import DjangoLocalDispatcher
from modules.fuel.integrations.auth_port import DjangoAuthAdapter
from .repositories import (
    DjangoVehicleRepository, 
    DjangoFuelRequestRepository
)

# --- USE CASES: VEÍCULOS ---
from modules.fuel.application.use_cases.vehicles.get_vehicle import GetVehicleUseCase
from modules.fuel.application.use_cases.vehicles.register_vehicle import RegisterVehicleUseCase
from modules.fuel.application.use_cases.vehicles.update_vehicle import UpdateVehicleUseCase

# --- USE CASES: REQUISIÇÕES V1 (INDIVIDUAIS) ---
from modules.fuel.application.use_cases.fuel_requests.approve_fuel import ApproveFuelUseCase
from modules.fuel.application.use_cases.fuel_requests.cancel_fuel import CancelFuelUseCase
from modules.fuel.application.use_cases.fuel_requests.fueling_completed import FuelingCompletedUseCase
from modules.fuel.application.use_cases.fuel_requests.list_fuel_requests import ListFuelRequestsUseCase
from modules.fuel.application.use_cases.fuel_requests.reject_fuel import RejectFuelUseCase
from modules.fuel.application.use_cases.fuel_requests.request_fuel import RequestFuelUseCase



# ==============================================================================
# FACTORY: VEÍCULOS (GESTÃO DE FROTA)
# ==============================================================================
class VehicleUseCaseFactory:
    @staticmethod
    def create_get_vehicle() -> GetVehicleUseCase:
        return GetVehicleUseCase(DjangoVehicleRepository())

    @staticmethod
    def create_register_vehicle() -> RegisterVehicleUseCase:
        return RegisterVehicleUseCase(DjangoVehicleRepository())

    @staticmethod
    def create_update_vehicle() -> UpdateVehicleUseCase:
        return UpdateVehicleUseCase(DjangoVehicleRepository())


# ==============================================================================
# FACTORY: FUEL REQUEST (V1 - INDIVIDUAL)
# ==============================================================================
class FuelRequestUseCaseFactory:
    @staticmethod
    def _get_common_deps():
        return {
            "fuel_repo": DjangoFuelRequestRepository(),
            "event_dispatcher": DjangoLocalDispatcher()
        }

    @staticmethod
    def create_request_fuel() -> RequestFuelUseCase:
        return RequestFuelUseCase(
            vehicle_repo=DjangoVehicleRepository(),
            **FuelRequestUseCaseFactory._get_common_deps()
        )

    @staticmethod
    def create_list_fuel_requests() -> ListFuelRequestsUseCase:
        return ListFuelRequestsUseCase(DjangoFuelRequestRepository())

    @staticmethod
    def create_approve_fuel() -> ApproveFuelUseCase:
        return ApproveFuelUseCase(
            user_provider=DjangoAuthAdapter(),
            **FuelRequestUseCaseFactory._get_common_deps()
        )

    @staticmethod
    def create_reject_fuel() -> RejectFuelUseCase:
        return RejectFuelUseCase(**FuelRequestUseCaseFactory._get_common_deps())

    @staticmethod
    def create_cancel_fuel() -> CancelFuelUseCase:
        return CancelFuelUseCase(**FuelRequestUseCaseFactory._get_common_deps())

    @staticmethod
    def create_fueling_completed() -> FuelingCompletedUseCase:
        return FuelingCompletedUseCase(**FuelRequestUseCaseFactory._get_common_deps())


