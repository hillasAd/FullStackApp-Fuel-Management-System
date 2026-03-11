from shared.exceptions.custom_exceptions import DomainException, ConflictException

class VehicleAlreadyRegistered(ConflictException):
    default_message = "Esta viatura já se encontra registada no sistema."
    error_code = "vehicle_already_exists"

class InvalidFuelStateTransition(DomainException):
    default_message = "Transição de estado não permitida para o estado atual do pedido."
    error_code = "invalid_fuel_state"

class TankCapacityExceeded(DomainException):
    default_message = "A quantidade solicitada excede a capacidade do tanque da viatura."
    error_code = "tank_capacity_exceeded"

class InvalidFuelAmountException(DomainException):
    default_message = "A quantidade de litros deve ser superior a zero e inferior ou igual a 200."
    error_code = "invalid_fuel_amount"
