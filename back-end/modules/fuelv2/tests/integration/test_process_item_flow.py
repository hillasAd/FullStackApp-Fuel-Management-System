import pytest
from unittest.mock import ANY, Mock
from modules.fuelv2.application.dtos import ProcessItemDTO
from modules.fuelv2.application.use_cases.fuel_requests.process_bulk_item import ProcessBulkItemUseCase

@pytest.mark.django_db
def test_process_use_case_should_dispatch_event_after_save(bulk_entity_factory):
    """
    Injetamos a 'bulk_entity_factory' como argumento do teste.
    O Pytest a encontrará automaticamente no conftest.py.
    """
    # Arrange
    mock_repo = Mock()
    mock_dispatcher = Mock()
    use_case = ProcessBulkItemUseCase(mock_repo, mock_dispatcher)
    
    # Criamos a entidade usando a factory (que agora foi injetada corretamente)
    # Garantimos que o item_id 1 existe no mock
    entity = bulk_entity_factory(id=10, items_count=2)
    # Atribuímos o ID manual ao primeiro item para bater com o DTO
    entity.items[0].id = 1 
    
    mock_repo.find_header_by_id.return_value = entity
    
    dto = ProcessItemDTO(
        bulk_id=10, 
        item_id=1, 
        admin_id=99, 
        action='APPROVED',
        version=1,  
        reason=None,
    )
    
    # Act
    use_case.execute(dto)
    
    # Assert
    assert mock_repo.save_item.called
    assert mock_repo.update_header_status.called
    
    # Verifica se o evento V2 foi disparado (usando o ANY que importou)
    # Nota: Verifique se o nome do evento no UseCase é exatamente 'fuel.item_approve_2'
    mock_dispatcher.dispatch.assert_called_with("fuelv2.item_approved_2", ANY)
