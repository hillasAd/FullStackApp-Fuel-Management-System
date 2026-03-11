import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import VehicleModel

@pytest.mark.django_db
def test_deve_bloquear_pedidos_em_excesso(api_client, user_token):
    # 1. Setup: Criar a viatura para o pedido ser VÁLIDO
    v = VehicleModel.objects.create(
        license_plate="LIMIT-01", 
        model="Test", 
        tank_capacity=200, 
        fuel_type="DIESEL"
    )
    
    url = reverse('fuel-request-v1-list-create')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    payload = {"vehicle_id": v.id, "liters": 1.0} # Pedido pequeno e válido

    # 2. Act: Disparar até estoirar o 'burst' (60/min)
    # Fazemos 61 para garantir que o 61º seja bloqueado
    for _ in range(60):
        api_client.post(url, payload, format='json')
    
    # O 61º disparo deve ser bloqueado pelo Throttling
    response = api_client.post(url, payload, format='json')
    data = response.json()
    
    # 3. Assert: Verificar se o status é 429 (Too Many Requests)
    assert response.status_code == 429
    # O código 'throttled' vem do DRF, vamos garantir que o teu handler o lê
    assert data["error"]["code"] == "throttled"
