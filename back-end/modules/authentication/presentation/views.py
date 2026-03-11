from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from modules.authentication.application.services import AuthenticationService
from shared.events.django_dispatcher import DjangoLocalDispatcher
from shared.responses.api_response import success
from .serializers import LoginSerializer, UserProfileSerializer
from rest_framework.throttling import ScopedRateThrottle

class LoginView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'sensitive'  # Aplica o limite de 5/minuto definido nas settings
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Criamos o dispatcher e passamos para o serviço
        dispatcher = DjangoLocalDispatcher()
        service = AuthenticationService(event_dispatcher=dispatcher)
        
        result = service.login_user(**serializer.validated_data)
        
        # Retornamos os tokens + dados básicos do usuário
        data = {
            **result["tokens"],
            "user": UserProfileSerializer(result["user"]).data
        }
        return success(data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        AuthenticationService.logout(refresh_token)
        return success(None, status=204)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # O DRF já validou o token e colocou o user no request
        serializer = UserProfileSerializer(request.user)
        return success(serializer.data)
