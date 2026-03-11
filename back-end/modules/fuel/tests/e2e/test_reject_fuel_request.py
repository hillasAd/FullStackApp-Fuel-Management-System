import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel

@pytest.mark.django_db
class TestRejectFuelRequestE2E:
    def test_manager_deve_rejeitar_pedido_pendente(self, api_client, manager_token):
        # Arrange
        v = VehicleModel.objects.create(license_plate="REJ-01", tank_capacity=60, fuel_type="DIESEL")
        req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=20, status="PENDING")
        
        url = reverse('fuel-request-v1-reject', kwargs={'pk': req.id})
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')

        # Act
        response = api_client.post(url)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "REJECTED"
        
        req.refresh_from_db()
        assert req.status == "REJECTED"
        assert req.rejected_by_id is not None
