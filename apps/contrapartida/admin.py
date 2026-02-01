from django.contrib import admin
from .models import Secretaria, Encaminhamento, Horas


@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ("nome", "sigla")
    search_fields = ("nome", "sigla")
    ordering = ("nome",)


@admin.register(Encaminhamento)
class EncaminhamentoAdmin(admin.ModelAdmin):
    list_display = ("numero", "aluno", "secretaria", "data", "responsavel_emissao")
    list_filter = ("secretaria", "data")
    search_fields = ("numero", "aluno__user__first_name", "aluno__user__last_name", "secretaria__sigla")
    raw_id_fields = ("aluno", "responsavel_emissao")
    autocomplete_fields = ("secretaria",)
    date_hierarchy = "data"
    ordering = ("-numero",)
    readonly_fields = ("numero",)


@admin.register(Horas)
class HorasAdmin(admin.ModelAdmin):
    list_display = ("aluno", "quantidade", "data_registro", "oficio_informacao", "responsavel_registro")
    list_filter = ("data_registro",)
    search_fields = ("oficio_informacao", "aluno__user__first_name", "aluno__user__last_name")
    raw_id_fields = ("aluno", "responsavel_registro")
    date_hierarchy = "data_registro"
    ordering = ("-data_registro",)
