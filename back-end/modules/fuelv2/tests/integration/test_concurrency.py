# modules/fuelv2/tests/integration/test_concurrency.py
import pytest
from modules.fuelv2.domain.entities import BulkStatus
from modules.fuelv2.infrastructure.repositories import DjangoBulkFuelRepository
from shared.exceptions.custom_exceptions import ConflictException

@pytest.mark.django_db
def test_repository_should_raise_conflict_on_stale_version(bulk_model_factory):
    """Testa se o banco bloqueia edições baseadas em versões antigas."""
    repo = DjangoBulkFuelRepository()
    model = bulk_model_factory(version=1) # Lote versão 1 no banco
    
    # Simula que o Admin A tenta atualizar usando a versão 1 (OK)
    repo.update_header_status(model.id, BulkStatus.PROCESSED, old_version=1)
    
    # Simula que o Admin B tenta atualizar usando a mesma versão 1 (Falha)
    with pytest.raises(ConflictException):
        repo.update_header_status(model.id, BulkStatus.CANCELLED, old_version=1)
