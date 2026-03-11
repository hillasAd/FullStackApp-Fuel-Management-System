from dataclasses import dataclass
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"

@dataclass
class NotificationPayload:
    recipient: str
    subject: str
    body: str
    notification_type: NotificationType
    context: dict = None
