import pytest
from unittest.mock import patch
from modules.notifications.application.services import NotificationService
from modules.notifications.domain.entities import NotificationPayload, NotificationType

class TestNotificationService:

    @patch("modules.notifications.infrastructure.providers.EmailProvider.send")
    def test_should_call_email_provider_when_type_is_email(self, mock_send):
        # Arrange
        service = NotificationService()
        payload = NotificationPayload(
            recipient="test@user.com",
            subject="Hello",
            body="World",
            notification_type=NotificationType.EMAIL
        )

        # Act
        service.notify(payload)

        # Assert
        mock_send.assert_called_once_with("test@user.com", "Hello", "World")
