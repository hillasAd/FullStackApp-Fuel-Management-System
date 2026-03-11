from django.db import models
from modules.fuel.infrastructure.models import VehicleModel
from ..domain.value_objects import BulkStatus, BulkItemStatus

class BulkFuelRequestModel(models.Model):
    """O Cabeçalho (Master) da Requisição de Lote (v2)"""
    requester_id = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    version = models.IntegerField(default=1)
    
    status = models.CharField(
        max_length=20, 
        default=BulkStatus.PENDING.value
    )
    
    cancellation_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fuel_requests_v2'
        ordering = ['-id']

class BulkFuelRequestItemModel(models.Model):
    """Os Itens (Detail) do Lote (v2)"""
    parent_request = models.ForeignKey(
        BulkFuelRequestModel, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    liters = models.FloatField()
    status = models.CharField(
        max_length=20, 
        default=BulkItemStatus.PENDING.value
    )
    
    # Auditoria e Rastreabilidade
    processed_by_id = models.IntegerField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'fuel_request_items_v2'
        ordering = ['-id']
