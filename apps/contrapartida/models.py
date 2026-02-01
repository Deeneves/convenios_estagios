from django.db import models
from apps.academico.models import Aluno
from apps.usuarios.models import User

#Modelo Secretaria
class Secretaria(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    sigla = models.CharField(max_length=10, verbose_name="Sigla")

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"
        ordering = ["nome"]

    def __str__(self):
        return self.sigla

#Modelo Encaminhamento
class Encaminhamento(models.Model):
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name="Secretaria")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="encaminhamentos", verbose_name="Aluno")
    data = models.DateField(verbose_name="Data")
    numero = models.IntegerField(verbose_name="Número", unique=True, auto_created=True)
    responsavel_emissao = models.ForeignKey(User, on_delete=models.CASCADE, related_name="encaminhamentos_emissao", verbose_name="Responsável pela emissão")

    class Meta:
        verbose_name = "Encaminhamento"
        verbose_name_plural = "Encaminhamentos"
        ordering = ["numero"]

    def __str__(self):
        return f"{self.numero} - {self.aluno.user.first_name} {self.aluno.user.last_name} - {self.secretaria.sigla}"

#Modelo Horas
class Horas(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="horas", verbose_name="Aluno")
    quantidade = models.DurationField(verbose_name="Quantidade de horas")
    data_registro = models.DateField(verbose_name="Data de registro")
    oficio_informacao = models.CharField(max_length=200, verbose_name="Ofício de informação")
    oficio_documento = models.FileField(upload_to="oficios/", verbose_name="Ofício de documento")
    responsavel_registro = models.ForeignKey(User, on_delete=models.CASCADE, related_name="horas_registro", verbose_name="Responsável pelo registro")

    class Meta:
        verbose_name = "Horas"
        verbose_name_plural = "Horas"
        ordering = ["data_registro"]

    def __str__(self):
        return f"{self.quantidade} - {self.encaminhamento.numero} - {self.encaminhamento.aluno.user.first_name} {self.encaminhamento.aluno.user.last_name} - {self.encaminhamento.secretaria.sigla}"
