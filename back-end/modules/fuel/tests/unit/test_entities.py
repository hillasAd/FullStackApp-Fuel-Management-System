import pytest
from modules.fuel.domain.entities import FuelRequest, Vehicle
from modules.fuel.domain.value_objects import FuelAmount, FuelType, FuelRequestStatus
from modules.fuel.domain.exceptions import TankCapacityExceeded, InvalidFuelStateTransition

def test_request_deve_validar_capacidade_do_tanque_mais_tolerancia_percentagem():
    v = Vehicle(1, "ABC-123", "Hilux", 80.0, FuelType.DIESEL)
    with pytest.raises(TankCapacityExceeded):
        FuelRequest(None, v, 10, FuelAmount(90.0))

def test_transicao_estado_invalida_deve_lancar_excecao():
    v = Vehicle(1, "ABC-123", "Hilux", 80.0, FuelType.DIESEL)
    req = FuelRequest(1, v, 10, FuelAmount(20.0), status=FuelRequestStatus.REJECTED)
    with pytest.raises(InvalidFuelStateTransition):
        req.approve(admin_id=99)
