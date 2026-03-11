from shared.exceptions.custom_exceptions import BaseAppException
from modules.fuel.domain.exceptions import TankCapacityExceeded, InvalidFuelStateTransition
from shared.exceptions.custom_exceptions import DomainException

def test_excecao_de_tanque_deve_ter_codigo_correto():
    exc = TankCapacityExceeded()
    assert isinstance(exc, BaseAppException)
    assert exc.error_code == "tank_capacity_exceeded"
    assert exc.status_code == 400

def test_excecoes_de_combustivel_devem_herdar_de_domain_exception():
    assert issubclass(TankCapacityExceeded, DomainException)
    assert issubclass(InvalidFuelStateTransition, DomainException)

def test_tank_capacity_exceeded_deve_ter_status_400():
    exc = TankCapacityExceeded()
    assert exc.status_code == 400
    assert exc.error_code == "tank_capacity_exceeded"
