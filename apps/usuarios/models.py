from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
    )
    username = models.CharField(
        "username",
        max_length=150,
        blank=True,
        null=True,
    )

    class Role(models.TextChoices):
        DIRETOR = "DIRETOR", "Diretor"
        ADMINISTRATIVO = "ADMINISTRATIVO", "Administrativo"
        ALUNO = "ALUNO", "Aluno"
        SECRETARIA = "SECRETARIA", "Secretaria"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ALUNO,
    )

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]
