from modules.dashboard.infrastructure.repositories import DjangoDashboardRepository

def test_repository_status_history_logic(db):

    repo = DjangoDashboardRepository()
    result = repo.get_aggregated_stats()
    
    assert "status_history" in result
    assert isinstance(result["status_history"], dict)
