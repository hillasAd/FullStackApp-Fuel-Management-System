from django.dispatch import Signal

# Definimos o evento: "Alguém logou com sucesso"
# Fornecemos o email e o username como contexto
user_logged_in_event = Signal()
