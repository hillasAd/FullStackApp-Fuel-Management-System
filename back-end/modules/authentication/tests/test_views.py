import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestLoginAPI:
    
    @pytest.fixture
    def create_user(self):
        return User.objects.create_user(
            username="testuser", 
            password="securepassword123", 
            email="test@example.com",
            role="USER"
        )

    def test_login_endpoint_success_format(self, client, create_user):
        url = reverse("login")
        payload = {"username": "testuser", "password": "securepassword123"}
        
        response = client.post(url, payload, content_type="application/json")
        data = response.json()

        # Asserting your custom 'success' structure
        assert response.status_code == status.HTTP_200_OK
        assert data["success"] is True
        assert "access" in data["data"]
        assert data["data"]["user"]["username"] == "testuser"
        assert data["error"] is None

    def test_login_endpoint_fail_format(self, client):
        url = reverse("login")
        payload = {"username": "wrong", "password": "wrong"}
        
        response = client.post(url, payload, content_type="application/json")
        data = response.json()

        # Asserting your custom 'error' structure from Exception Handler
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_credentials"
        assert "data" not in data or data["data"] is None

    def test_login_validation_error_format(self, client):
        url = reverse("login")
        payload = {"username": ""} # Empty username to trigger Serializer error
        
        response = client.post(url, payload, content_type="application/json")
        data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data["error"]["code"] == "validation_error"
        assert "username" in data["error"]["details"]
