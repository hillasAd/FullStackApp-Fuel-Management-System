import pytest
from django.urls import reverse
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel

@pytest.mark.django_db
class TestListFuelRequestsE2E:
    
    @pytest.fixture
    def setup_requests(self, create_user):
        # Criar dois condutores e um manager
        user1 = create_user(username="user1", role="USER")
        user2 = create_user(username="user2", role="USER")
        
        v = VehicleModel.objects.create(license_plate="LIST-01", tank_capacity=50, fuel_type="DIESEL")
        
        # Pedido do User 1
        FuelRequestModel.objects.create(vehicle=v, requester_id=user1.id, liters=10)
        # Pedido do User 2
        FuelRequestModel.objects.create(vehicle=v, requester_id=user2.id, liters=20)
        
        return user1, user2
       
    def test_condutor_deve_ver_apenas_os_seus_proprios_pedidos(self, api_client, user_token):
        # Obter o ID do user que o user_token representa
        from rest_framework_simplejwt.authentication import JWTAuthentication
        validated_token = JWTAuthentication().get_validated_token(user_token)
        user_id = validated_token['user_id']

        # Criar pedidos especificamente para este user_id
        v = VehicleModel.objects.create(license_plate="LIST-01", tank_capacity=50, fuel_type="DIESEL")
        FuelRequestModel.objects.create(vehicle=v, requester_id=user_id, liters=10) # Pedido DELE
        FuelRequestModel.objects.create(vehicle=v, requester_id=999, liters=20)     # Pedido de OUTRO

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        response = api_client.get(reverse('fuel-request-v1-list-create'))
        assert len(response.json()['results']) == 1 # Agora os IDs batem!


    def test_manager_deve_ver_todos_os_pedidos_do_sistema(self, api_client, manager_token, setup_requests):
        url = reverse('fuel-request-v1-list-create')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
        
        response = api_client.get(url)
        data = response.json()

        assert response.status_code == 200
        # O manager vê os 2 pedidos criados no setup
        assert len(data["results"]) == 2
