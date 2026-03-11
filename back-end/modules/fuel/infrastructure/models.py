from django.db import models
from modules.fuel.domain.value_objects import FuelRequestStatus, FuelType

# ==============================================================================
# VEÍCULOS
# ==============================================================================
class VehicleModel(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    tank_capacity = models.FloatField()
    fuel_type = models.CharField(
        max_length=20, 
        choices=[(tag.value, tag.name) for tag in FuelType]
    )
    version = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'fuel_vehicles'
        ordering = ['-id']

# ==============================================================================
# PEDIDOS INDIVIDUAIS
# ==============================================================================
class FuelRequestModel(models.Model):
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    requester_id = models.IntegerField()
    liters = models.FloatField()
    status = models.CharField(
        max_length=20, 
        choices=[(tag.value, tag.name) for tag in FuelRequestStatus],
        default=FuelRequestStatus.PENDING.value
    )
    
    # Auditoria V1
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by_id = models.IntegerField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejected_by_id = models.IntegerField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    fueled_at = models.DateTimeField(null=True, blank=True)
    fueled_by_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'fuel_requests_v1'
        ordering = ['-id']

