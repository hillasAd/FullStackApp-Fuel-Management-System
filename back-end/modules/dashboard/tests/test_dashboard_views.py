import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from ..presentation.views import DashboardStatsView
from ..domain.repositories import IDashboardRepository
from ..application.use_cases.fuel_request import GetDashboardSummaryUseCase

class MockDashboardRepository(IDashboardRepository):
    def get_aggregated_stats(self):
        return {
            "summary": {"total_liters": 300, "total_requests": 1, "pending": 0, "approved": 1},
            "weekly_flow":[],
            "fleet_performance": [],
            "recent_activities": [],
            "status_history":{},
            "fuel_distribution": {}
        }

@pytest.mark.django_db
def test_dashboard_view_returns_correct_data(create_user):
    # 1. Arrange
    factory = APIRequestFactory()
    request = factory.get('/api/v2/dashboard/summary/')
    
    # Criamos um usuário que satisfaça IsManager ou IsAdminRole
    user = create_user(username="test_manager", role="MANAGER")
    force_authenticate(request, user=user)
    
    # Injetamos o Mock
    mock_repo = MockDashboardRepository()
    mock_use_case = GetDashboardSummaryUseCase(mock_repo)
    view = DashboardStatsView.as_view(use_case=mock_use_case)

    # 2. Act
    response = view(request)
    
    # 3. Assert
    assert response.status_code == 200
    assert response.data["summary"]["total_liters"] == 300
