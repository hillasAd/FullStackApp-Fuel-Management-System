import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import VehicleModel, FuelRequestModel


@pytest.mark.django_db
def test_nao_deve_aprovar_o_mesmo_pedido_duas_vezes(api_client, manager_token):
    v = VehicleModel.objects.create(license_plate="IDEM-1", tank_capacity=100, fuel_type="DIESEL")
    req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=50, status="APPROVED") # Já aprovado

    url = f"/api/v1/requests/{req.id}/approve/"
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
    
    response = api_client.post(url)
    
    # Deve retornar erro de transição inválida (400) vindo do Domínio
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_fuel_state"



@pytest.mark.django_db
class TestIdempotency:
    def test_nao_deve_permitir_aprovar_pedido_ja_aprovado(self, api_client, manager_token):
        # Arrange: Criar um pedido que já está APPROVED
        v = VehicleModel.objects.create(license_plate="IDEM-01", tank_capacity=50, fuel_type="DIESEL")
        req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=10, status="APPROVED")
        
        url = reverse('fuel-request-v1-approve', kwargs={'pk': req.id})
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')

        # Act: Tentar aprovar novamente
        response = api_client.post(url)
        data = response.json()

        # Assert: Deve falhar com o erro de transição do Domínio
        assert response.status_code == 400
        assert data["error"]["code"] == "invalid_fuel_state"
        assert "Transição de estado não permitida" in data["error"]["message"]
