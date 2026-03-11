import pytest
from modules.fuel.domain.exceptions import InvalidFuelAmountException
from modules.fuel.domain.value_objects import FuelAmount

def test_fuel_amount_nao_pode_ser_negativo():
    with pytest.raises(InvalidFuelAmountException, match="A quantidade de litros deve ser superior a zero e inferior ou igual a 200."):
        FuelAmount(liters=-10)
