import pytest
from shared.exceptions.custom_exceptions import ConflictException

# INFRASTRUCTURE
from modules.fuelv2.infrastructure.repositories import DjangoBulkFuelRepository
from modules.fuelv2.infrastructure.models import BulkFuelRequestModel, BulkFuelRequestItemModel

# DOMAIN
from modules.fuelv2.domain.entities import BulkFuelRequest
from modules.fuelv2.domain.value_objects import BulkStatus 
from modules.fuel.domain.value_objects import FuelAmount

@pytest.mark.django_db
class TestBulkRepositoryIntegration:
    """
    Testes de Integração do Repositório Bulk.
    Valida persistência (Entidade -> Model) e mapeamento (Model -> Entidade).
    """

    def test_save_bulk_should_persist_aggregate_completely(self, dummy_vehicle_entity, vehicle_model):
        """Testa se o save_bulk grava o Header e todos os Itens no DB."""
        repo = DjangoBulkFuelRepository()
        
        dummy_vehicle_entity.id = vehicle_model.id
        
        # Arrange: Criar a raiz do agregado (Bulk)
        bulk = BulkFuelRequest(
            id=None,
            requester_id=1,
            description="Integration Test Bulk",
            items=[],
            version=1 
        )
        
        # Act: Adiciona itens usando a entidade com ID válido e salva
        bulk.add_item(dummy_vehicle_entity, FuelAmount(25.0))
        bulk.add_item(dummy_vehicle_entity, FuelAmount(35.0))
        
        saved_bulk = repo.save_bulk(bulk)

        # Assert: Entidade recebe IDs do banco
        assert saved_bulk.id is not None
        assert len(saved_bulk.items) == 2
        assert saved_bulk.items[0].id is not None
        
        # Assert: Registos existem nos Models Django
        db_model = BulkFuelRequestModel.objects.get(id=saved_bulk.id)
        assert db_model.description == "Integration Test Bulk"
        assert db_model.items.count() == 2

    def test_find_header_by_id_should_return_rich_entity(self, bulk_model_factory):
        """Testa o Mapper: verifica conversão Model -> Entidade com objetos aninhados."""
        repo = DjangoBulkFuelRepository()
        created_model = bulk_model_factory(items_count=3)

        # Act
        entity = repo.find_header_by_id(created_model.id)

        # Assert
        assert isinstance(entity, BulkFuelRequest)
        assert entity.id == created_model.id
        assert len(entity.items) == 3
        # Verifica reconstrução do veículo aninhado
        assert entity.items[0].vehicle.license_plate == "AB-01-MZ"
        assert isinstance(entity.status, BulkStatus)

    def test_update_header_status_should_respect_concurrency(self, bulk_model_factory):
        """Valida o Optimistic Locking (controlo de versão) no update de status."""
        repo = DjangoBulkFuelRepository()
        # Arrange: Lote versão 1 no banco
        model = bulk_model_factory(version=1)

        # Act: Update com a versão correta (deve passar)
        repo.update_header_status(model.id, BulkStatus.PROCESSED, old_version=1)
        
        model.refresh_from_db()
        assert model.status == "PROCESSED"
        assert model.version == 2 # Repositório deve incrementar a versão

        # Assert: Falha ao usar versão obsoleta (enviamos 1, mas agora é 2)
        with pytest.raises(ConflictException):
            repo.update_header_status(model.id, BulkStatus.CANCELLED, old_version=1)

    def test_save_item_should_persist_audit_fields(self, bulk_model_factory):
        """Testa se dados de aprovação (quem/quando) são persistidos no model do Item."""
        repo = DjangoBulkFuelRepository()
        model = bulk_model_factory(items_count=1)
        
        # Busca entidade via repo (mapeada do banco)
        item_entity = repo.find_item_by_id(model.items.first().id)
        
        # Act: Aprova e salva
        item_entity.approve(admin_id=500)
        repo.save_item(item_entity)
        
        # Assert: DB reflete as mudanças
        db_item = BulkFuelRequestItemModel.objects.get(id=item_entity.id)
        assert db_item.status == "APPROVED"
        assert db_item.processed_by_id == 500
        assert db_item.processed_at is not None
