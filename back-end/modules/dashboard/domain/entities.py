from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DashboardStats:
    fuel_distribution: dict
    fleet_performance: list
    recent_activities: list
    summary: Dict
    weekly_flow: List
    
    
