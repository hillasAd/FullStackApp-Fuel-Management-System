import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import Throttled
from shared.exceptions.custom_exceptions import BaseAppException

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Primeiro tenta o handler padrão do DRF (ele captura 404, 405, 401, 403 nativos)
    response = drf_exception_handler(exc, context)

    # 1. Caso seja excecção de domínio (BaseAppException)
    if isinstance(exc, BaseAppException):
        logger.warning(f"Application error: {exc.error_code}", extra={"error": str(exc)})
        return Response(
            {"success": False, "error": {"code": exc.error_code, "message": exc.message}},
            status=exc.status_code
        )

    # 2. Tratar especificamente o Throttling (Anti-Spam)
    if isinstance(exc, Throttled):
        logger.warning("User throttled", extra={"wait": exc.wait})
        return Response(
            {
                "success": False,
                "error": {
                    "code": "throttled",
                    "message": "Limite de requisições excedido.",
                    "details": f"Tente novamente em {exc.wait} segundos."
                }
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # 3. Melhoria aqui: Capturar 404, 405 e ValidationErrors do DRF de forma inteligente
    if response is not None:
        logger.warning("DRF handled exception", extra={"status": response.status_code, "detail": response.data})
        
        # Mapeamento dinâmico de códigos de erro
        error_mapping = {
            status.HTTP_404_NOT_FOUND: "not_found",
            status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
            status.HTTP_401_UNAUTHORIZED: "unauthorized",
            status.HTTP_403_FORBIDDEN: "permission_denied",
            status.HTTP_400_BAD_REQUEST: "validation_error",
        }
        
        error_code = error_mapping.get(response.status_code, "api_error")
        
        # Extrair mensagem amigável (o DRF costuma usar a chave 'detail')
        message = "Invalid request"
        if isinstance(response.data, dict):
            message = response.data.get("detail", message)
        elif isinstance(response.data, list):
            message = response.data[0]

        return Response(
            {
                "success": False,
                "error": {
                    "code": error_code,
                    "message": message,
                    "details": response.data
                }
            },
            status=response.status_code
        )

    # 4. Erro inesperado (500 real)
    logger.exception("Unhandled exception", exc_info=exc)
    return Response(
        {
            "success": False,
            "error": {"code": "internal_server_error", "message": "An unexpected error occurred"}
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
