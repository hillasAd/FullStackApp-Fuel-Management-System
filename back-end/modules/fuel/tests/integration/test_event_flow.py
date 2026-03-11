import pytest
from django.core import mail
from shared.events.django_dispatcher import DjangoLocalDispatcher

@pytest.mark.django_db
def test_fluxo_de_evento_entre_fuel_e_notifications(api_client):
    
    mail.outbox = []
    dispatcher = DjangoLocalDispatcher()
    
    dispatcher.dispatch("fuel.request_created", {
        "request_id": 1, 
        "vehicle_plate": "ABC", 
        "liters": 10,
        "user_email": "gestor@teste.com"
    })
    
    # Prova que Notifications ouviu Fuel
    assert len(mail.outbox) > 0 
