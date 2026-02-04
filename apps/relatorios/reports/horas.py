"""Relatórios de horas."""

from django.db.models import Q, Sum

from apps.academico.models import Aluno
from apps.contrapartida.models import Horas
from core.utils.formatters import format_duracao_horas


def relatorio_horas_dados(filtros=None):
    """
    Retorna colunas e linhas para o relatório detalhado de horas.

    Args:
        filtros: dict com data_inicio, data_fim, aluno_id (opcional)

    Returns:
        tuple: (colunas, linhas)
    """
    colunas = ["Aluno", "Quantidade", "Data registro", "Ofício informação", "Responsável"]

    queryset = Horas.objects.select_related(
        "aluno__user", "responsavel_registro"
    ).order_by("-data_registro")

    if filtros:
        data_inicio = filtros.get("data_inicio")
        data_fim = filtros.get("data_fim")
        aluno_id = filtros.get("aluno_id")

        if data_inicio:
            queryset = queryset.filter(data_registro__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_registro__lte=data_fim)
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)

    linhas = []
    for h in queryset:
        nome_aluno = f"{h.aluno.user.first_name or ''} {h.aluno.user.last_name or ''}".strip()
        if not nome_aluno:
            nome_aluno = str(h.aluno.user)
        responsavel = f"{h.responsavel_registro.first_name or ''} {h.responsavel_registro.last_name or ''}".strip()
        if not responsavel:
            responsavel = str(h.responsavel_registro)
        linhas.append(
            [
                nome_aluno,
                format_duracao_horas(h.quantidade),
                h.data_registro.strftime("%d/%m/%Y"),
                h.oficio_informacao or "—",
                responsavel,
            ]
        )

    return colunas, linhas


def relatorio_horas_por_aluno_dados(filtros=None):
    """
    Retorna colunas e linhas para o relatório de total de horas por aluno.

    Args:
        filtros: dict com data_inicio, data_fim (opcional)

    Returns:
        tuple: (colunas, linhas)
    """
    colunas = ["Aluno", "Matrícula", "Curso", "Total de horas"]

    base = Aluno.objects.filter(horas__isnull=False)
    if filtros:
        data_inicio = filtros.get("data_inicio")
        data_fim = filtros.get("data_fim")
        if data_inicio:
            base = base.filter(horas__data_registro__gte=data_inicio)
        if data_fim:
            base = base.filter(horas__data_registro__lte=data_fim)

    alunos_com_horas = (
        base.annotate(total=Sum("horas__quantidade"))
        .select_related("user", "curso")
        .order_by("user__first_name", "user__last_name")
        .distinct()
    )

    linhas = []
    for aluno in alunos_com_horas:
        nome = f"{aluno.user.first_name or ''} {aluno.user.last_name or ''}".strip()
        if not nome:
            nome = str(aluno.user)
        matricula = aluno.matricula or "—"
        curso = aluno.curso.nome if aluno.curso else "—"
        total = getattr(aluno, "total", None)
        total_str = format_duracao_horas(total) if total else "0:00:00"
        linhas.append([nome, matricula, curso, total_str])

    return colunas, linhas
