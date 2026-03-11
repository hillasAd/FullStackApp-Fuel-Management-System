import pytest
from rest_framework import status
from modules.fuelv2.domain.value_objects import BulkItemStatus
from modules.fuelv2.infrastructure.models import BulkFuelRequestModel, BulkFuelRequestItemModel

@pytest.mark.django_db
class TestBulkFuelAPI:
    """
    Testes de Ponta-a-Ponta (E2E) para o Módulo Bulk (V2).
    Valida o fluxo desde o Request HTTP até a persistência final no Banco.
    """

    def test_create_bulk_request_api_flow(self, api_client, user_token, vehicle_model):
        """POST /api/v2/requests/bulk/create/ - Fluxo Completo de Criação"""
        # Arrange
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        url = '/api/v2/requests/bulk/create/'
        payload = {
            "description": "Lote Semanal de Teste",
            "items": [
                {"vehicle_id": vehicle_model.id, "liters": 50.0}
            ]
        }

        # Act
        response = api_client.post(url, payload, format='json')

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['status'] == "PENDING"
        assert len(response.data['data']['items']) == 1
        
        # Verifica integridade no DB
        assert BulkFuelRequestModel.objects.count() == 1
        assert BulkFuelRequestItemModel.objects.count() == 1

    def test_get_bulk_detail_with_items(self, api_client, user_token, bulk_model_factory):
        """GET /api/v2/requests/bulk/<pk>/ - Detalhes do Lote"""
        # Arrange
        bulk_model = bulk_model_factory(items_count=3)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        url = f'/api/v2/requests/bulk/{bulk_model.id}/'

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']['items']) == 3
        # Verifica se o serializer mapeou a placa via entidade
        assert response.data['data']['items'][0]['license_plate'] == "AB-01-MZ"

    def test_process_item_approve_flow_requirement_4(self, api_client, manager_token, bulk_model_factory):
        """POST .../process/ - Aprovação Granular (Requisito 4)"""
        # Arrange
        bulk_model = bulk_model_factory(items_count=1)
        item_id = bulk_model.items.first().id
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
        
        url = f'/api/v2/requests/bulk/{bulk_model.id}/items/{item_id}/process/'
        payload = {
            "action": "APPROVED",
            "version": bulk_model.version
        }

        # Act
        response = api_client.post(url, payload, format='json')

        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        # Verify DB changes via Model
        item_db = BulkFuelRequestItemModel.objects.get(id=item_id)
        assert item_db.status == BulkItemStatus.APPROVED.value
        assert item_db.processed_by_id is not None

    def test_process_item_concurrency_conflict(self, api_client, manager_token, bulk_model_factory):
        """Valida se a API retorna 409 Conflict em caso de versão obsoleta"""
        # Arrange
        bulk_model = bulk_model_factory(version=1)
        item_id = bulk_model.items.first().id
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
        
        url = f'/api/v2/requests/bulk/{bulk_model.id}/items/{item_id}/process/'
        payload = {
            "action": "APPROVED", 
            "version": 0
        }

        # Act
        response = api_client.post(url, payload, format='json')

        # Assert
        response_content = str(response.data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "alterado por outro usuário" in response_content
        