from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        trim_whitespace=False,
        required=True
    )
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    # Campos calculados para facilitar a vida do Frontend
    permissions = serializers.SerializerMethodField()
    display_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'display_name',
            'role',
            'permissions', 
            'is_active'
        ]
        read_only_fields = fields

    def get_permissions(self, obj):
        """
        Retorna uma lista de strings com as permissões reais do Django 
        ex: ['view_user', 'add_project']
        """
        return [p.split('.')[-1] for p in obj.get_all_permissions()]
