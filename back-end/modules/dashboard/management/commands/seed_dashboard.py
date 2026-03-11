import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

# Models conforme sua estrutura de módulos
from modules.fuel.infrastructure.models import VehicleModel
from modules.fuelv2.infrastructure.models import BulkFuelRequestModel, BulkFuelRequestItemModel
from modules.fuel.infrastructure.models import FuelRequestModel
from modules.fuelv2.domain.value_objects import BulkItemStatus, BulkStatus

class Command(BaseCommand):
    help = 'Seed Completo: 10 Viaturas + 2000 V2 + 500 V1 (Limite 200L)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO("🚀 Iniciando Seed Global com trava de 200L..."))

        try:
            with transaction.atomic():
                # 1. VIATURAS (fuel_vehicles)
                v_data = [
                    ('LDA-10-20', 'Toyota Hilux', 80.0, 'DIESEL'),
                    ('AFG-45-MZ', 'Ford Ranger', 80.0, 'DIESEL'),
                    ('MZA-12-34', 'Fuso Canter', 120.0, 'DIESEL'),
                    ('TRK-99-00', 'Volvo FH', 400.0, 'DIESEL'),
                    ('GAS-01-01', 'Honda City', 45.0, 'GASOLINE'),
                    ('GAS-02-02', 'Toyota Corolla', 50.0, 'GASOLINE'),
                    ('GAS-03-03', 'Hyundai Accent', 45.0, 'GASOLINE'),
                    ('TRK-88-11', 'Scania R500', 450.0, 'DIESEL'),
                    ('YTR-44-22', 'Mitsubishi Fuso', 150.0, 'DIESEL'),
                    ('BBA-99-11', 'Nissan NP200', 50.0, 'GASOLINE'),
                ]

                vehicles = []
                for plate, model, cap, f_type in v_data:
                    v, _ = VehicleModel.objects.update_or_create(
                        license_plate=plate,
                        defaults={'model': model, 'tank_capacity': cap, 'fuel_type': f_type, 'version': 1}
                    )
                    vehicles.append(v)
                
                self.stdout.write(f"✅ {len(vehicles)} Viaturas prontas.")

                now = timezone.now()
                status_v2 = [s.value for s in BulkItemStatus]

                # 2. SEED V2 (2000 REGISTROS)
                for i in range(2000):
                    days_ago = i % 8
                    date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
                    item_status = random.choice(status_v2)
                    
                    parent_status = BulkStatus.COMPLETED.value if item_status == 'FUELED' else BulkStatus.PENDING.value

                    # Criar Pai V2
                    request_parent = BulkFuelRequestModel(
                        requester_id=1,
                        description=f"Lote Automatizado V2 #{i+1}",
                        version=2,
                        status=parent_status,
                        created_at=date,
                        updated_at=date
                    )
                    request_parent.save()

                    # Criar Item V2 com trava de 200L
                    v = random.choice(vehicles)
                    liters_calc = round(random.uniform(v.tank_capacity * 0.2, v.tank_capacity * 0.9), 2)
                    liters = min(liters_calc, 200.0)

                    BulkFuelRequestItemModel.objects.create(
                        parent_request=request_parent,
                        vehicle=v,
                        liters=liters,
                        status=item_status,
                        processed_at=date if item_status == 'FUELED' else None
                    )

                self.stdout.write("✅ 2000 registros V2 inseridos.")

                # 3. SEED V1 (500 REGISTROS)
                for j in range(500):
                    days_ago = j % 15
                    date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
                    v = random.choice(vehicles)
                    st_v1 = random.choice(status_v2)

                    # Cálculo Litros V1 com trava de 200L
                    liters_v1_calc = round(random.uniform(10, v.tank_capacity * 0.7), 2)
                    liters_v1 = min(liters_v1_calc, 200.0)

                    fuel_request_v1 = FuelRequestModel(
                        vehicle=v,
                        requester_id=1,
                        liters=liters_v1,
                        status=st_v1,
                        created_at=date
                    )

                    # Auditoria V1
                    if st_v1 == 'FUELED': fuel_request_v1.fueled_at = date
                    elif st_v1 == 'APPROVED': fuel_request_v1.approved_at = date
                    elif st_v1 == 'REJECTED': fuel_request_v1.rejected_at = date
                    elif st_v1 == 'CANCELLED': fuel_request_v1.cancelled_at = date
                    
                    fuel_request_v1.save()

                self.stdout.write("✅ 500 registros V1 inseridos.")

            self.stdout.write(self.style.SUCCESS("🎯 Radar Sincronizado! 2500 registros totais (Máx 200L)."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 Falha: {str(e)}"))
            self.stdout.write(self.style.WARNING("🔄 Rollback executado. DB limpa."))
