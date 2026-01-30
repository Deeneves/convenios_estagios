from datetime import date

from django.conf import settings
from django.db import models


class Faculdade(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")

    class Meta:
        verbose_name = "Faculdade"
        verbose_name_plural = "Faculdades"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    faculdade = models.ForeignKey(
        Faculdade,
        on_delete=models.CASCADE,
        related_name="cursos",
        verbose_name="Faculdade",
    )
    duracao = models.PositiveIntegerField(
        verbose_name="Duração (semestres)",
        help_text="Duração do curso em semestres",
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    class EstadoCivil(models.TextChoices):
        SOLTEIRO = "SOLTEIRO", "Solteiro(a)"
        CASADO = "CASADO", "Casado(a)"
        DIVORCIADO = "DIVORCIADO", "Divorciado(a)"
        VIUVO = "VIUVO", "Viúvo(a)"
        UNIAO_ESTAVEL = "UNIAO_ESTAVEL", "União estável"

    class Situacao(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="aluno",
        verbose_name="Usuário",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="alunos",
        verbose_name="Curso",
        null=True,
        blank=True,
    )
    matricula = models.CharField(
        max_length=50,
        verbose_name="Matrícula",
        unique=True,
        null=True,
        blank=True,
    )
    data_ingresso = models.DateField(
        verbose_name="Data de ingresso",
        null=True,
        blank=True,
    )
    situacao = models.CharField(
        max_length=10,
        choices=Situacao.choices,
        verbose_name="Situação",
        default=Situacao.ATIVO,
    )
    data_nascimento = models.DateField(
        verbose_name="Data de nascimento",
        null=True,
        blank=True,
    )
    rg = models.CharField(
        max_length=20,
        verbose_name="RG",
        null=True,
        blank=True,
    )
    estado_civil = models.CharField(
        max_length=20,
        choices=EstadoCivil.choices,
        verbose_name="Estado civil",
        null=True,
        blank=True,
    )
    logradouro = models.CharField(
        max_length=200,
        verbose_name="Logradouro",
        null=True,
        blank=True,
    )
    numero = models.CharField(
        max_length=20,
        verbose_name="Número",
        null=True,
        blank=True,
    )
    complemento = models.CharField(
        max_length=100,
        verbose_name="Complemento",
        null=True,
        blank=True,
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro",
        null=True,
        blank=True,
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade",
        null=True,
        blank=True,
    )
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado (UF)",
        null=True,
        blank=True,
    )
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["user"]

    def semestre_atual(self):
        if not self.data_ingresso:
            return None
        ingresso_idx = self.data_ingresso.year * 2 + (1 if self.data_ingresso.month <= 6 else 2)
        hoje = date.today()
        hoje_idx = hoje.year * 2 + (1 if hoje.month <= 6 else 2)
        semestre = hoje_idx - ingresso_idx + 1
        if semestre < 1:
            return None
        return semestre

    def __str__(self):
        return str(self.user)
