import pytest
from django.core import mail
from shared.events.django_dispatcher import DjangoLocalDispatcher

@pytest.mark.django_db
class TestEventIntegration:
    def test_sinal_de_login_deve_disparar_envio_de_email_em_outro_modulo(self):
        # 1. Arrange: Limpa a caixa de saída e define os dados
        mail.outbox = []
        email_teste = "hilario@exemplo.com"
        username_teste = "hilario_admin"
        
        # Obtemos o dispatcher (o "grito" do sistema)
        dispatcher = DjangoLocalDispatcher()

        # 2. Act: Disparamos o evento como o AuthenticationService faria
        # O módulo de Notifications deve estar "ouvindo" isso via apps.py
        dispatcher.dispatch(
            event_name="user_logged_in",
            payload={
                "user_email": email_teste,
                "username": username_teste
            }
        )

        # 3. Assert: Verificamos se a integração funcionou entre os módulos
        assert len(mail.outbox) == 1
        sent_email = mail.outbox[0]
        
        assert sent_email.subject == "Alerta de Segurança"
        assert email_teste in sent_email.to
        assert username_teste in sent_email.body
