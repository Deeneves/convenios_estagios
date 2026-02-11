"""Views para geração de relatórios em PDF e XLSX. Uso: incluir links/botões nos templates (ex.: lista de alunos)."""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from apps.contrapartida.models import Encaminhamento
from apps.usuarios.models import User

from .reports import (
    relatorio_alunos_dados,
    relatorio_encaminhamentos_dados,
    relatorio_horas_dados,
    relatorio_horas_por_aluno_dados,
    relatorio_consolidado_dados,
)
from .services import gerar_pdf_tabela, gerar_pdf_documento, gerar_xlsx_tabela


def relatorios_required(view_func):
    """Decorator que permite acesso apenas a DIRETOR, ADMINISTRATIVO ou superuser."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if not (
            request.user.is_superuser
            or request.user.role in [User.Role.DIRETOR, User.Role.ADMINISTRATIVO]
        ):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped


def _extrair_filtros(request, campos):
    """Extrai filtros do GET em um dict."""
    filtros = {}
    for campo in campos:
        valor = request.GET.get(campo)
        if valor:
            filtros[campo] = valor
    return filtros or None


# --- Alunos ---


@login_required
@relatorios_required
def relatorio_alunos_pdf(request):
    filtros = _extrair_filtros(request, ["q", "matricula", "curso", "situacao"])
    colunas, linhas = relatorio_alunos_dados(filtros)
    pdf_bytes = gerar_pdf_tabela("Lista de Alunos", colunas, linhas)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_alunos.pdf"'
    return response


@login_required
@relatorios_required
def relatorio_alunos_xlsx(request):
    filtros = _extrair_filtros(request, ["q", "matricula", "curso", "situacao"])
    colunas, linhas = relatorio_alunos_dados(filtros)
    xlsx_bytes = gerar_xlsx_tabela("Lista de Alunos", colunas, linhas)
    response = HttpResponse(
        xlsx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="relatorio_alunos.xlsx"'
    return response


# --- Encaminhamentos ---


@login_required
@relatorios_required
def relatorio_encaminhamentos_pdf(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim"])
    colunas, linhas = relatorio_encaminhamentos_dados(filtros)
    pdf_bytes = gerar_pdf_tabela(
        "Encaminhamentos por Período", colunas, linhas, orientacao="landscape"
    )
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_encaminhamentos.pdf"'
    return response


@login_required
@relatorios_required
def relatorio_encaminhamentos_xlsx(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim"])
    colunas, linhas = relatorio_encaminhamentos_dados(filtros)
    xlsx_bytes = gerar_xlsx_tabela("Encaminhamentos", colunas, linhas)
    response = HttpResponse(
        xlsx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="relatorio_encaminhamentos.xlsx"'
    return response


@login_required
def encaminhamento_pdf(request, pk):
    """Gera PDF de um único encaminhamento (template oficial FALS)."""
    from .services.encaminhamento_pdf import gerar_pdf_encaminhamento

    enc = get_object_or_404(
        Encaminhamento.objects.select_related(
            "aluno__user", "aluno__curso", "secretaria", "responsavel_emissao"
        ),
        pk=pk,
    )
    pdf_bytes = gerar_pdf_encaminhamento(enc)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="encaminhamento_{enc.numero}.pdf"'
    return response


# --- Horas (detalhado) ---


@login_required
@relatorios_required
def relatorio_horas_pdf(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim", "aluno_id"])
    colunas, linhas = relatorio_horas_dados(filtros)
    pdf_bytes = gerar_pdf_tabela(
        "Registro de Horas (Detalhado)", colunas, linhas, orientacao="landscape"
    )
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_horas.pdf"'
    return response


@login_required
@relatorios_required
def relatorio_horas_xlsx(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim", "aluno_id"])
    colunas, linhas = relatorio_horas_dados(filtros)
    xlsx_bytes = gerar_xlsx_tabela("Registro de Horas", colunas, linhas)
    response = HttpResponse(
        xlsx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="relatorio_horas.xlsx"'
    return response


# --- Horas por aluno ---


@login_required
@relatorios_required
def relatorio_horas_por_aluno_pdf(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim"])
    colunas, linhas = relatorio_horas_por_aluno_dados(filtros)
    pdf_bytes = gerar_pdf_tabela("Horas por Aluno", colunas, linhas)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_horas_por_aluno.pdf"'
    return response


@login_required
@relatorios_required
def relatorio_horas_por_aluno_xlsx(request):
    filtros = _extrair_filtros(request, ["data_inicio", "data_fim"])
    colunas, linhas = relatorio_horas_por_aluno_dados(filtros)
    xlsx_bytes = gerar_xlsx_tabela("Horas por Aluno", colunas, linhas)
    response = HttpResponse(
        xlsx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="relatorio_horas_por_aluno.xlsx"'
    return response


# --- Consolidado (apenas PDF) ---


@login_required
@relatorios_required
def relatorio_consolidado_pdf(request):
    colunas, linhas = relatorio_consolidado_dados()
    pdf_bytes = gerar_pdf_tabela("Relatório Consolidado", colunas, linhas)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_consolidado.pdf"'
    return response
