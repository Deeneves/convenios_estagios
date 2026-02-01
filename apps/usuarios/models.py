from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError("O CPF deve ser informado.")

        cpf = str(cpf).strip()

        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(cpf, password, **extra_fields)

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self._create_user(cpf, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        DIRETOR = "DIRETOR", "Diretor"
        ADMINISTRATIVO = "ADMINISTRATIVO", "Administrativo"
        ALUNO = "ALUNO", "Aluno"
        SECRETARIA = "SECRETARIA", "Secretaria"

    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="username",
    )
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ALUNO,
    )

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
