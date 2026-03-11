import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_erro_de_validacao_deve_seguir_formato_shared(api_client):
    url = "/api/v1/vehicles/"
    # Enviando payload vazio para forçar erro de serializer
    response = api_client.post(url, {}, content_type='application/json')
    
    data = response.json()
    assert data["success"] is False
    assert "code" in data["error"]
    assert "details" in data["error"]


@pytest.mark.django_db
class TestErrorResponseFormat:
    def test_formato_de_erro_de_validacao_drf_deve_ser_padronizado(self, api_client, user_token):
        url = reverse('vehicle-list-create')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
        
        # Enviar payload vazio para disparar ValidationError
        response = api_client.post(url, {}, content_type='application/json')
        data = response.json()

        # Assert: O formato deve ser o do teu Custom Exception Handler
        assert data["success"] is False
        assert "error" in data
        assert data["error"]["code"] == "validation_error"
        assert "details" in data["error"]
