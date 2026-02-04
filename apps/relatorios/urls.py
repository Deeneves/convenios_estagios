from django.urls import path

from . import views

app_name = "relatorios"

urlpatterns = [
    # Alunos
    path("alunos/pdf/", views.relatorio_alunos_pdf, name="alunos_pdf"),
    path("alunos/xlsx/", views.relatorio_alunos_xlsx, name="alunos_xlsx"),
    # Encaminhamentos
    path("encaminhamentos/pdf/", views.relatorio_encaminhamentos_pdf, name="encaminhamentos_pdf"),
    path("encaminhamentos/xlsx/", views.relatorio_encaminhamentos_xlsx, name="encaminhamentos_xlsx"),
    path("encaminhamento/<int:pk>/pdf/", views.encaminhamento_pdf, name="encaminhamento_pdf"),
    # Horas (detalhado)
    path("horas/pdf/", views.relatorio_horas_pdf, name="horas_pdf"),
    path("horas/xlsx/", views.relatorio_horas_xlsx, name="horas_xlsx"),
    # Horas por aluno
    path("horas-por-aluno/pdf/", views.relatorio_horas_por_aluno_pdf, name="horas_por_aluno_pdf"),
    path("horas-por-aluno/xlsx/", views.relatorio_horas_por_aluno_xlsx, name="horas_por_aluno_xlsx"),
    # Consolidado
    path("consolidado/pdf/", views.relatorio_consolidado_pdf, name="consolidado_pdf"),
]
