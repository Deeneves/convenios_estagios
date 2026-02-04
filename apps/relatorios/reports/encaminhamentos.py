"""Relatório de encaminhamentos por período."""

from django.db.models import Q

from apps.contrapartida.models import Encaminhamento


def relatorio_encaminhamentos_dados(filtros=None):
    """
    Retorna colunas e linhas para o relatório de encaminhamentos.

    Args:
        filtros: dict com data_inicio, data_fim (opcional)

    Returns:
        tuple: (colunas, linhas)
    """
    colunas = ["Número", "Aluno", "Secretaria", "Data", "Responsável emissão"]

    queryset = Encaminhamento.objects.select_related(
        "aluno__user", "secretaria", "responsavel_emissao"
    ).order_by("-data", "-numero")

    if filtros:
        data_inicio = filtros.get("data_inicio")
        data_fim = filtros.get("data_fim")

        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)

    linhas = []
    for enc in queryset:
        nome_aluno = f"{enc.aluno.user.first_name or ''} {enc.aluno.user.last_name or ''}".strip()
        if not nome_aluno:
            nome_aluno = str(enc.aluno.user)
        responsavel = f"{enc.responsavel_emissao.first_name or ''} {enc.responsavel_emissao.last_name or ''}".strip()
        if not responsavel:
            responsavel = str(enc.responsavel_emissao)
        linhas.append(
            [
                enc.numero,
                nome_aluno,
                enc.secretaria.sigla,
                enc.data.strftime("%d/%m/%Y"),
                responsavel,
            ]
        )

    return colunas, linhas
