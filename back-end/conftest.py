import pytest
from datetime import datetime
from unittest.mock import Mock

from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

# --- Imports de Domínio (V1 e V2) ---
from modules.fuel.domain.entities import Vehicle
from modules.fuel.domain.value_objects import FuelAmount, FuelType, FuelRequestStatus
from modules.fuelv2.domain.entities import BulkFuelRequest, BulkFuelRequestItem

# --- Imports de Infraestrutura (Models) ---
from modules.fuel.infrastructure.models import VehicleModel
from modules.fuelv2.infrastructure.models import BulkFuelRequestModel, BulkFuelRequestItemModel

from modules.fuelv2.domain.value_objects import BulkStatus

User = get_user_model()

# ==============================================================================
# 1. AUTENTICAÇÃO E CLIENTES API (GLOBAIS)
# ==============================================================================

@pytest.fixture
def api_client():
    """Cliente DRF para testes E2E."""
    return APIClient()

@pytest.fixture
def create_user(db):
    """Helper para criar utilizadores com roles customizadas."""
    def make_user(username, role="USER"):
        return User.objects.create_user(
            username=username,
            password="password123",
            email=f"{username}@empresa.com",
            role=role
        )
    return make_user

@pytest.fixture
def user_token(create_user):
    user = create_user(username="condutor_comum", role="USER")
    return str(RefreshToken.for_user(user).access_token)

@pytest.fixture
def manager_token(create_user):
    user = create_user(username="gestor_fuel", role="MANAGER")
    return str(RefreshToken.for_user(user).access_token)

@pytest.fixture
def operator_token(create_user):
    user = create_user(username="operador_01", role="OPERATOR")
    return str(RefreshToken.for_user(user).access_token)

# ==============================================================================
# 2. FIXTURES DE DOMÍNIO (MEMÓRIA - UNITÁRIOS)
# ==============================================================================

@pytest.fixture
def dummy_vehicle_entity():
    """Entidade de Veículo para lógica de domínio pura."""
    return Vehicle(
        id=1,
        license_plate="AB-01-MZ",
        model="Toyota Hilux",
        tank_capacity=80.0,
        fuel_type=FuelType.DIESEL,
        version=1
    )

@pytest.fixture
def bulk_entity_factory(dummy_vehicle_entity):
    """Gera Agregados BulkFuelRequest. Uso: bulk = bulk_entity_factory()"""
    def _make_bulk(id=1, items_count=2, status=BulkStatus.PENDING):
        bulk = BulkFuelRequest(
            id=id,
            requester_id=10,
            description="Lote de Teste Unidade",
            items=[],
            status=BulkStatus.PENDING,
            version=1,
            created_at=timezone.now()
        )
        for i in range(items_count):
            bulk.add_item(dummy_vehicle_entity, FuelAmount(20.0))
            bulk.items[i].id = i + 100
        
        bulk.status = status 
        return bulk
    return _make_bulk

# ==============================================================================
# 3. FIXTURES DE INFRAESTRUTURA (BANCO - INTEGRAÇÃO/E2E)
# ==============================================================================

@pytest.fixture
def vehicle_model(db):
    """Model Django de Veículo persistido."""
    return VehicleModel.objects.create(
        license_plate="AB-01-MZ",
        model="Toyota Hilux",
        tank_capacity=80.0,
        fuel_type='DIESEL',
        version=1
    )

@pytest.fixture
def bulk_model_factory(db, vehicle_model):
    """Model Django de Lote persistido."""
    def _make_model(items_count=1, status='PENDING', version=1):
        header = BulkFuelRequestModel.objects.create(
            requester_id=1,
            description="Lote Persistido no DB",
            status=status,
            version=version
        )
        for _ in range(items_count):
            BulkFuelRequestItemModel.objects.create(
                parent_request=header,
                vehicle=vehicle_model,
                liters=30.0,
                status=FuelRequestStatus.PENDING.value
            )
        return header
    return _make_model

# ==============================================================================
# 4. MOCKS DE COMPONENTES
# ==============================================================================

@pytest.fixture
def mock_event_dispatcher():
    return Mock()

@pytest.fixture
def mock_bulk_repo():
    return Mock()
