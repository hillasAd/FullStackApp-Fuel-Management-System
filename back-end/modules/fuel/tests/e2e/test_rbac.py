import pytest


@pytest.mark.django_db
def test_condutor_nao_pode_aprovar_proprio_pedido(api_client, user_token):
    # Simula um user com role 'USER' tentando acessar rota de 'MANAGER'
    url = "/api/v1/requests/1/approve/"
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    
    response = api_client.post(url)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "permission_denied"
