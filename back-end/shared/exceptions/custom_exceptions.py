# shared/exceptions/custom_exceptions.py

class BaseAppException(Exception):
    """
    Excecção base da aplicação.
    Nunca deve ser lançada diretamente.
    """

    status_code = 400
    default_message = "Application error"
    error_code = "application_error"

    def __init__(self, message=None, error_code=None):
        self.message = message or self.default_message
        self.error_code = error_code or self.error_code
        super().__init__(self.message)


class DomainException(BaseAppException):
    status_code = 400
    default_message = "Domain validation error"
    error_code = "domain_error"


class NotFoundException(BaseAppException):
    status_code = 404
    default_message = "Resource not found"
    error_code = "not_found"


class PermissionDeniedException(BaseAppException):
    status_code = 403
    default_message = "Permission denied"
    error_code = "permission_denied"


class ConflictException(BaseAppException):
    status_code = 409
    default_message = "Conflict error"
    error_code = "conflict"


class UnauthorizedException(BaseAppException):
    status_code = 401
    default_message = "Unauthorized"
    error_code = "unauthorized"