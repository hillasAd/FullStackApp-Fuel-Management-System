from shared.exceptions.custom_exceptions import UnauthorizedException


class InvalidCredentials(UnauthorizedException):
    default_message = "Invalid username or password"
    error_code = "invalid_credentials"