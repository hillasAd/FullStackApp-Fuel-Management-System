import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import VehicleModel, FuelRequestModel

@pytest.mark.django_db
class TestCreateFuelRequestE2E:
    def test_condutor_deve_criar_pedido_com_sucesso(self, api_client, user_token):
        # Arrange
        v = VehicleModel.objects.create(license_plate="TEST-01", model="Hilux", tank_capacity=80, fuel_type="DIESEL")
        url = reverse('fuel-request-v1-list-create')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        payload = {"vehicle_id": v.id, "liters": 40.0}

        # Act
        response = api_client.post(url, payload, format='json')
        data = response.json()

        # Assert
        assert response.status_code == 201
        assert data["success"] is True
        assert data["data"]["status"] == "PENDING"
        assert FuelRequestModel.objects.filter(vehicle=v, liters=40.0).exists()

    def test_deve_falhar_se_exceder_capacidade_do_tanque(self, api_client, user_token):
        v = VehicleModel.objects.create(license_plate="TEST-02", model="Mini", tank_capacity=30, fuel_type="GASOLINE")
        url = reverse('fuel-request-v1-list-create')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        payload = {"vehicle_id": v.id, "liters": 35.0}

        response = api_client.post(url, payload, format='json')
        
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "tank_capacity_exceeded"
