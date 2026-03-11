from ..domain.entities import NotificationPayload, NotificationType
from ..infrastructure.providers import EmailProvider, SMSProvider

class NotificationService:
    def __init__(self):
        self.providers = {
            NotificationType.EMAIL: EmailProvider(),
            NotificationType.SMS: SMSProvider()
        }

    def notify(self, payload: NotificationPayload):
        provider = self.providers.get(payload.notification_type)
        if provider:
            return provider.send(payload.recipient, payload.subject, payload.body)
        return False
