import pytest
from unittest.mock import patch
from modules.notifications.application.services import NotificationService
from modules.notifications.domain.entities import NotificationPayload, NotificationType

class TestSMSService:
    @patch("modules.notifications.infrastructure.providers.SMSProvider.send")
    def test_deve_chamar_provedor_sms_quando_tipo_for_sms(self, mock_sms_send):
        # Arrange
        service = NotificationService()
        payload = NotificationPayload(
            recipient="+258840000000",
            subject="Código",
            body="Seu código é 1234",
            notification_type=NotificationType.SMS
        )

        # Act
        service.notify(payload)

        # Assert
        mock_sms_send.assert_called_once_with("+258840000000", "Código", "Seu código é 1234")
