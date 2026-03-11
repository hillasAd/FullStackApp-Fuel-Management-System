import structlog
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from modules.authentication.domain.exceptions import InvalidCredentials
from shared.exceptions.custom_exceptions import DomainException, UnauthorizedException
from shared.events.dispatcher import EventDispatcher

# Inicializa o logger estruturado
logger = structlog.get_logger(__name__)

class AuthenticationService:
    def __init__(self, event_dispatcher: EventDispatcher):
        self.event_dispatcher = event_dispatcher

    def login_user(self, username, password):
        # O structlog herda o correlation_id do seu middleware automaticamente
        logger.info("auth_attempt", username=username)

        user = authenticate(username=username, password=password)
        
        if not user:
            logger.warning("auth_failed", username=username, reason="invalid_credentials")
            # Sua exceção que herda de UnauthorizedException
            raise InvalidCredentials()

        if not user.is_active:
            logger.warning("auth_failed", user_id=user.id, reason="inactive_user")
            raise UnauthorizedException("Usuário desativado pelo administrador")

        # Gera os tokens
        tokens = AuthenticationService.generate_tokens(user)

        # Log de sucesso com contexto rico
        logger.info(
            "auth_success", 
            user_id=user.id, 
            role=user.role,
            ip_info="logged" # Você poderia extrair isso do request se quisesse
        )
 
        try:
            # DISPARO DO EVENTO (O módulo de Auth termina aqui a sua responsabilidade)
            # O Service apenas "anuncia" o fato ocorrido
            self.event_dispatcher.dispatch(
                event_name="user_logged_in",
                payload={
                    "user_email": user.email,
                    "username": user.username,
                }
            )
        
        except Exception as e:
            # Não deixamos um erro de notificação travar o login do usuário
            logger.error("event_dispatch_failed", error=str(e))
            
        return {
            "user": user,
            "tokens": tokens
        }

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        # Adicionamos claims customizados no token se necessário
        refresh["role"] = user.role 
        
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        
    @staticmethod
    def logout(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            # Se o token for inválido, ignoramos ou lançamos erro de domínio
            raise DomainException("Token inválido ou já expirado")
