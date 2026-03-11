import pytest


@pytest.mark.django_db
def test_admin_can_reject_single_item_with_reason(api_client, bulk_model_factory,manager_token):
    bulk_model = bulk_model_factory() # Lote com 2 itens PENDING
    item_to_reject = bulk_model.items.first()
    
    # 2. Autenticação: Injetar o token do gestor no cliente
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {manager_token}')
    
    url = f'/api/v2/requests/bulk/{bulk_model.id}/items/{item_to_reject.id}/process/'
    payload = {
        "action": "REJECTED",
        "reason": "Viatura em manutenção",
        "version": bulk_model.version
    }
    
    response = api_client.post(url, payload, format='json')
    
    assert response.status_code == 200
    # Verifica se o item no banco mudou para REJECTED
    item_to_reject.refresh_from_db()
    assert item_to_reject.status == "REJECTED"
    assert item_to_reject.rejection_reason == "Viatura em manutenção"
