from django.apps import AppConfig
from shared.events.django_dispatcher import DjangoLocalDispatcher
from .application import event_handlers


class NotificationsConfig(AppConfig):
    name = 'modules.notifications'
    label = 'notifications'

    def ready(self):
        
        # Conectando os sinais do módulo Fuel
        DjangoLocalDispatcher.get_signal("user_logged_in").connect(event_handlers.on_user_logged_in)

        # Eventos do Módulo Fuel
        DjangoLocalDispatcher.get_signal("fuel.request_created").connect(event_handlers.on_fuel_request_created)
        DjangoLocalDispatcher.get_signal("fuel.request_approved").connect(event_handlers.on_fuel_request_approved)
        DjangoLocalDispatcher.get_signal("fuel.request_rejected").connect(event_handlers.on_fuel_request_rejected)
