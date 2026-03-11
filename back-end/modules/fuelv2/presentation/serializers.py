from rest_framework import serializers

class BulkFuelItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    vehicle_id = serializers.IntegerField(source='vehicle.id')    
    license_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)
    model_name = serializers.CharField(source='vehicle.model', read_only=True)
    liters = serializers.FloatField(source='amount.liters')
    status = serializers.CharField(source='status.value', read_only=True)
    
    processed_at = serializers.DateTimeField(read_only=True)
    processed_by_id = serializers.IntegerField(read_only=True)
    rejection_reason = serializers.CharField(read_only=True)

class BulkFuelRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    requester_id = serializers.IntegerField(required=False)
    description = serializers.CharField(allow_blank=True, required=False)  
    status = serializers.CharField(source='status.value', read_only=True)
    cancellation_reason = serializers.CharField(read_only=True)
    version = serializers.IntegerField(default=1)
    items = BulkFuelItemSerializer(many=True)
    
    created_at = serializers.DateTimeField(read_only=True)
    total_items = serializers.SerializerMethodField()

    def get_total_items(self, obj) -> int:
        if isinstance(obj, dict):
            return len(obj.get('items', []))
        return len(obj.items)



class BulkActionProcessSerializer(serializers.Serializer):
    """Serializer exclusivo para validar o comando de ação global ou individual"""
    action = serializers.CharField(required=True)
    version = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=False, allow_blank=True, default="")
