from django.contrib import admin
from .models import Aluno, Curso, Faculdade


@admin.register(Faculdade)
class FaculdadeAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nome", "faculdade", "duracao")
    list_filter = ("faculdade",)
    search_fields = ("nome", "faculdade__nome")
    ordering = ("nome",)
    autocomplete_fields = ("faculdade",)


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "get_user_cpf", "curso", "situacao", "cidade", "estado")
    list_filter = ("situacao", "estado_civil", "curso__faculdade", "curso")
    search_fields = ("matricula", "user__cpf", "user__email", "user__first_name", "user__last_name", "cidade")
    ordering = ("matricula",)
    autocomplete_fields = ("user", "curso")

    fieldsets = (
        (
            "Dados acadêmicos",
            {
                "fields": ("user", "curso", "matricula", "situacao"),
            },
        ),
        (
            "Dados pessoais",
            {
                "fields": ("data_nascimento", "rg", "estado_civil"),
            },
        ),
        (
            "Endereço",
            {
                "fields": (
                    "logradouro",
                    "numero",
                    "complemento",
                    "bairro",
                    "cidade",
                    "estado",
                    "cep",
                ),
            },
        ),
    )

    @admin.display(description="CPF")
    def get_user_cpf(self, obj):
        return obj.user.cpf if obj.user_id else "—"
