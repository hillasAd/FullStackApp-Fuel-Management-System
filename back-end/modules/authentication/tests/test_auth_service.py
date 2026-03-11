import pytest
from unittest.mock import patch, MagicMock
from modules.authentication.application.services import AuthenticationService
from shared.exceptions.custom_exceptions import UnauthorizedException

class TestAuthenticationService:

    # IMPORTANT: Patch the 'authenticate' that was imported INSIDE your services.py
    @patch("modules.authentication.application.services.authenticate")
    def test_login_user_with_invalid_credentials_raises_exception(self, mock_auth):
        # Arrange
        mock_auth.return_value = None

        # Act & Assert
        with pytest.raises(UnauthorizedException) as exc:
            AuthenticationService.login_user(self, username="wrong", password="password")
        
        assert exc.value.error_code == "invalid_credentials"
        mock_auth.assert_called_once_with(username="wrong", password="password")

    @patch("modules.authentication.application.services.AuthenticationService.generate_tokens")
    @patch("modules.authentication.application.services.authenticate")
    def test_login_user_success_returns_data(self, mock_auth, mock_gen_tokens):
        # Arrange
        mock_user = MagicMock(is_active=True, id=1, role="ADMIN")
        mock_auth.return_value = mock_user
        mock_gen_tokens.return_value = {"access": "token_abc", "refresh": "refresh_abc"}

        # Act
        result = AuthenticationService.login_user(self,"admin", "pass")

        # Assert
        assert result["user"] == mock_user
        assert result["tokens"]["access"] == "token_abc"
        mock_auth.assert_called_once()
