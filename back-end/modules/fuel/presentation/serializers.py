from rest_framework import serializers
from ..domain.value_objects import FuelType

class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    license_plate = serializers.CharField(max_length=20)
    model = serializers.CharField(max_length=100)
    tank_capacity = serializers.FloatField()
    fuel_type = serializers.ChoiceField(choices=[tag.value for tag in FuelType])
    version = serializers.IntegerField(read_only=True)

class FuelRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.IntegerField(write_only=True)
    requester_id = serializers.IntegerField(read_only=True)
    liters = serializers.FloatField(source='amount.liters') 
    status = serializers.CharField(source='status.value', read_only=True)
    
    created_at = serializers.DateTimeField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)
    fueled_at = serializers.DateTimeField(read_only=True)