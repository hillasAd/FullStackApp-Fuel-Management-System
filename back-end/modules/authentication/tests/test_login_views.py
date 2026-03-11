import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_login_success():
    User.objects.create_user(username="test", password="123456")
    client = APIClient()

    response = client.post("/api/v1/auth/login/", {
        "username": "test",
        "password": "123456"
    }, format="json")

    assert response.status_code == 200
    assert response.data["success"] is True
    assert "access" in response.data["data"]


@pytest.mark.django_db
def test_login_invalid_credentials():
    User.objects.create_user(username="test", password="123456")
    client = APIClient()

    response = client.post("/api/v1/auth/login/", {
        "username": "test",
        "password": "wrong"
    }, format="json")

    assert response.status_code == 401
    assert response.data["success"] is False
    assert response.data["error"]["code"] == "invalid_credentials"