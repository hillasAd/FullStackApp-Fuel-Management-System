from abc import ABC, abstractmethod

class IDashboardRepository(ABC):
    @abstractmethod
    def get_aggregated_stats(self) -> dict: pass