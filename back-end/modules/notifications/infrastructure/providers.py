import abc
import structlog
from django.core.mail import send_mail
from django.conf import settings

logger = structlog.get_logger(__name__)

class BaseNotificationProvider(abc.ABC):
    @abc.abstractmethod
    def send(self, recipient: str, subject: str, body: str):
        pass

class EmailProvider(BaseNotificationProvider):
    def send(self, recipient: str, subject: str, body: str):
        logger.info("sending_email", recipient=recipient, subject=subject)
        return send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

class SMSProvider(BaseNotificationProvider):
    def send(self, recipient: str, subject: str, body: str):
        # Implementation for Twilio/MessageBird/etc.
        logger.info("sending_sms_mock", recipient=recipient)
        return True
