import pytest
from unittest.mock import MagicMock
from modules.dashboard.application.use_cases.fuel_request import GetDashboardSummaryUseCase

def test_use_case_returns_correct_structure():
    mock_repo = MagicMock()
    expected_data = {
        "summary": {"total_liters": 100},
        "weekly_flow": [],
        "fleet_performance": [],
        "recent_activities": []
    }
    mock_repo.get_aggregated_stats.return_value = expected_data
    
    use_case = GetDashboardSummaryUseCase(mock_repo)
    result = use_case.execute()
    
    assert result == expected_data
    mock_repo.get_aggregated_stats.assert_called_once()
    
    
