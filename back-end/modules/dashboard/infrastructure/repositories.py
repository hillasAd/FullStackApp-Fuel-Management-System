from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from modules.fuelv2.infrastructure.models import BulkFuelRequestItemModel
from modules.fuel.infrastructure.models import VehicleModel
from modules.fuelv2.domain.value_objects import BulkItemStatus
from ..domain.repositories import IDashboardRepository

class DjangoDashboardRepository(IDashboardRepository):
    def get_aggregated_stats(self) -> dict:
        today = timezone.now()
        start_date = today - timedelta(days=6)

        # 1. Status Operacional (Dicionário para Cards)
        status_qs = BulkFuelRequestItemModel.objects.values('status').annotate(
            count=Count('id')
        )
        status_history = {item['status']: item['count'] for item in status_qs}

        # 2. Fluxo Semanal (L) - Apenas o que já foi abastecido
        weekly_qs = BulkFuelRequestItemModel.objects.filter(
            status=BulkItemStatus.FUELED.value,
            processed_at__gte=start_date
        ).annotate(
            day=TruncDay('processed_at')
        ).values('day').annotate(
            total_liters=Sum('liters')
        ).order_by('day')

        # 3. Resumo Geral (Cards de Topo)
        # Adicionado filtro explícito para garantir que o número de pendentes seja real
        stats = BulkFuelRequestItemModel.objects.aggregate(
            total_liters=Sum('liters', filter=Q(status=BulkItemStatus.FUELED.value)),
            total_requests=Count('id'),
            # Garante que o card de topo tenha o número exato global
            total_pending=Count('id', filter=Q(status=BulkItemStatus.PENDING.value))
        )

        # 4. Performance da Frota (RELATÓRIO DETALHADO POR ESTADO)
        # Adicionei os filtros Q para contar cada estado individualmente por viatura
        fleet = VehicleModel.objects.annotate(
            pending_count=Count('bulkfuelrequestitemmodel', filter=Q(bulkfuelrequestitemmodel__status=BulkItemStatus.PENDING.value)),
            approved_count=Count('bulkfuelrequestitemmodel', filter=Q(bulkfuelrequestitemmodel__status=BulkItemStatus.APPROVED.value)),
            rejected_count=Count('bulkfuelrequestitemmodel', filter=Q(bulkfuelrequestitemmodel__status=BulkItemStatus.REJECTED.value)),
            req_completed=Count('bulkfuelrequestitemmodel', filter=Q(bulkfuelrequestitemmodel__status=BulkItemStatus.FUELED.value)),
            liters_total=Sum('bulkfuelrequestitemmodel__liters', filter=Q(bulkfuelrequestitemmodel__status=BulkItemStatus.FUELED.value))
        ).values(
            'license_plate', 'model', 'fuel_type', 
            'pending_count', 'approved_count', 'rejected_count', 
            'req_completed', 'liters_total'
        ).order_by('-liters_total')

        # 5. Atividades Recentes
        recent = BulkFuelRequestItemModel.objects.select_related('vehicle').order_by('-id')[:5]
        
        # 6. Distribuição por Combustível
        fuel_dist_qs = BulkFuelRequestItemModel.objects.filter(
            status=BulkItemStatus.FUELED.value
        ).values('vehicle__fuel_type').annotate(
            total=Sum('liters')
        )
        fuel_distribution = {item['vehicle__fuel_type']: item['total'] for item in fuel_dist_qs}

        return {
            "summary": {
                "total_liters": stats['total_liters'] or 0,
                "total_requests": stats['total_requests'],
                "total_pending": stats['total_pending'],
            },
            "status_history": status_history,
            "weekly_flow": list(weekly_qs),
            "fleet_performance": list(fleet),
            "recent_activities": recent,
            "fuel_distribution": fuel_distribution
        }
