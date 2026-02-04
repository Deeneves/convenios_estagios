"""Relatório consolidado (resumo geral)."""

from apps.academico.models import Aluno, Curso, Faculdade
from apps.contrapartida.models import Encaminhamento, Horas
from django.db.models import Sum


def relatorio_consolidado_dados(filtros=None):
    """
    Retorna colunas e linhas para o relatório consolidado (apenas PDF).

    Args:
        filtros: não usado no consolidado (mostra totais gerais)

    Returns:
        tuple: (colunas, linhas)
    """
    colunas = ["Indicador", "Quantidade"]

    total_alunos = Aluno.objects.count()
    total_alunos_ativos = Aluno.objects.filter(situacao="ATIVO").count()
    total_faculdades = Faculdade.objects.count()
    total_cursos = Curso.objects.count()
    total_encaminhamentos = Encaminhamento.objects.count()
    total_horas_registros = Horas.objects.count()
    soma_horas = Horas.objects.aggregate(total=Sum("quantidade"))["total"]
    total_horas_str = "0:00:00"
    if soma_horas:
        from core.utils.formatters import format_duracao_horas
        total_horas_str = format_duracao_horas(soma_horas)

    linhas = [
        ["Total de alunos", total_alunos],
        ["Alunos ativos", total_alunos_ativos],
        ["Faculdades", total_faculdades],
        ["Cursos", total_cursos],
        ["Encaminhamentos", total_encaminhamentos],
        ["Registros de horas", total_horas_registros],
        ["Soma total de horas", total_horas_str],
    ]

    return colunas, linhas
