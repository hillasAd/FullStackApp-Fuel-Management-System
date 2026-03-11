import pytest
from django.db import transaction
from modules.fuel.infrastructure.models import FuelRequestModel, VehicleModel

@pytest.mark.django_db
def test_transacao_deve_fazer_rollback_se_evento_falhar_criticamente():
    # Este teste garante que se o DB salvar mas algo explodir antes do commit,
    vehicle = VehicleModel.objects.create(license_plate="TEST-01", tank_capacity=50, fuel_type="DIESEL")
    
    try:
        with transaction.atomic():
            FuelRequestModel.objects.create(vehicle=vehicle, requester_id=1, liters=10, status="PENDING")
            raise Exception("Erro forçado para testar rollback")
    except:
        pass

    assert FuelRequestModel.objects.count() == 0 # Prova o Rollback


import pytest
from django.db import transaction
from modules.fuel.infrastructure.models import VehicleModel

@pytest.mark.django_db
class TestTransactions:
    def test_rollback_no_registo_de_viatura_se_ocorrer_erro_inesperado(self):
        # Simulamos uma operação atómica que falha no fim simulando o lancamento duma excepcao
        try:
            with transaction.atomic():
                VehicleModel.objects.create(license_plate="ROLL-01", tank_capacity=60, fuel_type="DIESEL")
                # Forçamos um erro após o insert
                raise Exception("Erro catastrófico de infraestrutura")
        except:
            pass

        # Assert: A viatura não deve existir na DB
        assert VehicleModel.objects.filter(license_plate="ROLL-01").count() == 0
