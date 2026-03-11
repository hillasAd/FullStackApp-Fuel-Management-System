from unittest.mock import MagicMock
from modules.fuel.application.use_cases.fuel_requests.approve_fuel import ApproveFuelUseCase
from modules.fuel.application.use_cases.fuel_requests.list_fuel_requests import ListFuelRequestsUseCase
from modules.fuel.domain.value_objects import FuelRequestStatus

def test_approve_use_case_deve_chamar_repo_e_dispatcher():
    # Arrange
    repo = MagicMock()
    dispatcher = MagicMock()
    user_provider = MagicMock() # <--- O novo membro do arsenal
    
    # Mockando o comportamento do pedido e do provedor de user
    mock_request = MagicMock(status=FuelRequestStatus.PENDING)
    mock_request.requester_id = 1
    repo.find_by_id.return_value = mock_request
    
    # Mockando o retorno do user_provider
    user_provider.get_user_contact_info.return_value = {
        "user_email": "teste@teste.com", 
        "username": "tester"
    }
    
    # Act: Agora passamos os 3 argumentos
    use_case = ApproveFuelUseCase(repo, dispatcher, user_provider)
    use_case.execute(request_id=1, admin_id=99)
    
    # Assert
    assert repo.save.called
    assert dispatcher.dispatch.called
    user_provider.get_user_contact_info.assert_called_once_with(1)



def test_list_fuel_requests_deve_chamar_repositorio_com_filtros():
    # Arrange
    mock_repo = MagicMock()
    use_case = ListFuelRequestsUseCase(fuel_repo=mock_repo)
    filters = {"requester_id": 1}

    # Act
    use_case.execute(filters)

    # Assert
    mock_repo.list_all.assert_called_once_with(filters)
