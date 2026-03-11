from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        MANAGER = "MANAGER", "Manager"
        OPERATOR = "OPERATOR", "Operator"
        USER = "USER", "Standard User"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, 
        choices=Roles.choices, 
        default=Roles.USER
    )
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Usaremos o email como campo de login principal se desejar, 
    # mas aqui manteremos compatibilidade com o username.
    REQUIRED_FIELDS = ["email"] 

    def __str__(self):
        return f"{self.username} ({self.role})"
