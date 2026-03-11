import abc

class UserProviderPort(abc.ABC):
    @abc.abstractmethod
    def get_user_contact_info(self, user_id: int) -> dict: 
        """Retorna {'email': ..., 'username': ...}"""
        pass
