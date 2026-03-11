import pytest
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel


@pytest.mark.django_db
def test_fluxo_de_aprovacao_pelo_manager(api_client, manager_token):
    # 1. Setup: Pedido Pendente na DB
    v = VehicleModel.objects.create(license_plate="BOSS-1", tank_capacity=100, fuel_type="DIESEL")
    req = FuelRequestModel.objects.create(vehicle=v, requester_id=1, liters=50, status="PENDING")

    url = f"/api/v1/requests/{req.id}/approve/"
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
    
    # 2. Act
    response = api_client.post(url)
    
    # 3. Assert
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "APPROVED"
    assert "approved_at" in response.json()["data"]
