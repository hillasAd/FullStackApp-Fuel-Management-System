from django.dispatch import Signal
from .dispatcher import EventDispatcher

# Dicionário global para mapear nomes de strings para objetos Signal reais
_signals_registry = {}

class DjangoLocalDispatcher(EventDispatcher):
    def dispatch(self, event_name: str, payload: dict):
        if event_name not in _signals_registry:
            _signals_registry[event_name] = Signal()
        
        # Dispara o sinal internamente
        _signals_registry[event_name].send(sender=self.__class__, **payload)

    @staticmethod
    def get_signal(event_name: str) -> Signal:
        if event_name not in _signals_registry:
            _signals_registry[event_name] = Signal()
        return _signals_registry[event_name]

def receiver(event_name: str):
    """
    Decorador customizado para registrar funções no registro de sinais 
    baseado no nome da string do evento.
    """
    def decorator(func):
        signal = DjangoLocalDispatcher.get_signal(event_name)
        # Conecta a função ao sinal do Django
        signal.connect(func)
        return func
    return decorator