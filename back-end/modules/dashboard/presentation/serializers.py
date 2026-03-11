from rest_framework import serializers
from modules.fuelv2.infrastructure.models import BulkFuelRequestItemModel

class DashboardRecentActivitySerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField(source='vehicle.license_plate')
    vehicle_model = serializers.CharField(source='vehicle.model')
    fuel_type = serializers.CharField(source='vehicle.fuel_type')

    class Meta:
        model = BulkFuelRequestItemModel
        fields = ['id', 'vehicle', 'vehicle_model', 'liters', 'status', 'fuel_type']


class WeeklyFlowSerializer(serializers.Serializer):
    day = serializers.DateTimeField(format="%d/%m")
    total_liters = serializers.FloatField()

class DashboardResponseSerializer(serializers.Serializer):
    summary = serializers.DictField()
    weekly_flow = WeeklyFlowSerializer(many=True)
    fleet_performance = serializers.ListField()
    recent_activities = DashboardRecentActivitySerializer(many=True)
    status_history = serializers.DictField()
    fuel_distribution = serializers.DictField()