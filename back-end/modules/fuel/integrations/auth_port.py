from django.contrib.auth import get_user_model
from ..domain.services import UserProviderPort

User = get_user_model()

class DjangoAuthAdapter(UserProviderPort):
    def get_user_contact_info(self, user_id: int) -> dict:
        try:
            user = User.objects.get(id=user_id)
            return {
                "user_email": user.email,
                "username": user.username
            }
        except User.DoesNotExist:
            return {"user_email": "sistema@empresa.com", "username": "Desconhecido"}
