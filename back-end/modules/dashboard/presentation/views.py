from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shared.permission import IsAdminRole
from .serializers import DashboardResponseSerializer
from modules.dashboard.application.use_cases.fuel_request import GetDashboardSummaryUseCase
from ..infrastructure.repositories import DjangoDashboardRepository
from modules.fuel.presentation.permissions import IsManager
  
    
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated & (IsAdminRole | IsManager)]
    use_case = None

    def get(self, request):
        current_use_case = self.use_case or GetDashboardSummaryUseCase(DjangoDashboardRepository())
        raw_data = current_use_case.execute()
        
        serializer = DashboardResponseSerializer(raw_data)
        return Response(serializer.data)

