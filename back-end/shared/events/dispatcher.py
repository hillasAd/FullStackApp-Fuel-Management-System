import abc

class EventDispatcher(abc.ABC):
    @abc.abstractmethod
    def dispatch(self, event_name: str, payload: dict):
        """Dispara um evento com um nome e dados serializáveis."""
        pass
