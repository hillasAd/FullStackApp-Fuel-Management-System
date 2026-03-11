from .services import NotificationService
from ..domain.entities import NotificationPayload, NotificationType
import structlog

logger = structlog.get_logger(__name__)

def on_user_logged_in(sender, **kwargs):
    """
    Este é o Subscriber. Ele reage ao sinal vindo do Auth.
    """
    user_email = kwargs.get("user_email")
    username = kwargs.get("username")

    service = NotificationService()
    payload = NotificationPayload(
        recipient=user_email,
        subject="Alerta de Segurança",
        body=f"Olá {username}, um novo login foi detectado.",
        notification_type=NotificationType.EMAIL
    )
    service.notify(payload)



def on_fuel_request_created(sender, **kwargs):
    """Notifica o GESTOR que há um novo pedido pendente."""
    service = NotificationService()
    payload = NotificationPayload(
        recipient=kwargs.get("user_email"),
        subject="Novo Pedido de Combustível",
        body=f"Viatura: {kwargs.get('vehicle_plate')} | Litros: {kwargs.get('liters')}",
        notification_type=NotificationType.EMAIL
    )
    service.notify(payload)
    logger.info("notification_sent_fuel_request", request_id=kwargs.get("request_id"))

def on_fuel_request_approved(sender, **kwargs):
    """Notifica o CONDUTOR que o seu pedido foi aprovado."""
    service = NotificationService()
    payload = NotificationPayload(
        recipient=kwargs.get("user_email"),
        subject="Pedido de Combustível Aprovado",
        body=f"O teu pedido {kwargs.get('request_id')} foi aprovado. Podes abastecer.",
        notification_type=NotificationType.EMAIL
    )
    service.notify(payload)

def on_fuel_request_rejected(sender, **kwargs):
    """Notifica o CONDUTOR da rejeição."""
    service = NotificationService()
    payload = NotificationPayload(
        recipient=kwargs.get("user_email"),
        subject="Pedido de Combustível Rejeitado",
        body=f"O teu pedido {kwargs.get('request_id')} foi rejeitado pelo gestor.",
        notification_type=NotificationType.EMAIL
    )
    service.notify(payload)
