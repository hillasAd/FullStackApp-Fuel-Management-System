import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel

@pytest.mark.django_db
class TestCompleteFuelRequestE2E:
    def test_deve_concluir_abastecimento_apos_aprovacao(self, api_client, operator_token):
       
        # Arrange: Pedido já aprovado (APPROVED)
        v = VehicleModel.objects.create(license_plate="FULL-01", tank_capacity=100, fuel_type="GASOLINE")
        req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=50, status="APPROVED")
        
        url = reverse('fuel-request-v1-complete', kwargs={'pk': req.id})
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {operator_token}')

        # Act
        response = api_client.post(url)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "FUELED"
        assert "fueled_at" in response.json()["data"]

    def test_nao_deve_concluir_abastecimento_se_ainda_estiver_pendente(self, api_client, operator_token):
        v = VehicleModel.objects.create(license_plate="FAIL-01", tank_capacity=100, fuel_type="GASOLINE")
        req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=50, status="PENDING")
        
        url = reverse('fuel-request-v1-complete', kwargs={'pk': req.id})
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {operator_token}')

        response = api_client.post(url)
        
        # Deve falhar porque a transição PENDING -> FUELED é proibida
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid_fuel_state"
