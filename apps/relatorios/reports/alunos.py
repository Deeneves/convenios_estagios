"""Relatório de lista de alunos."""

from django.db.models import Q

from apps.academico.models import Aluno


def relatorio_alunos_dados(filtros=None):
    """
    Retorna colunas e linhas para o relatório de alunos.

    Args:
        filtros: dict com q, matricula, curso, situacao (opcional)

    Returns:
        tuple: (colunas, linhas)
    """
    colunas = ["Nome", "CPF", "Matrícula", "Curso", "Faculdade", "Semestre", "Situação"]

    queryset = Aluno.objects.select_related("user", "curso", "curso__faculdade").order_by(
        "user__first_name", "user__last_name"
    )

    if filtros:
        q = filtros.get("q", "").strip()
        matricula = filtros.get("matricula", "").strip()
        curso_id = filtros.get("curso")
        situacao = filtros.get("situacao", "").strip()

        if q:
            queryset = queryset.filter(
                Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(user__cpf__icontains=q)
                | Q(matricula__icontains=q)
            )
        if matricula:
            queryset = queryset.filter(matricula__icontains=matricula)
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if situacao:
            queryset = queryset.filter(situacao=situacao)

    linhas = []
    for aluno in queryset:
        nome = f"{aluno.user.first_name or ''} {aluno.user.last_name or ''}".strip() or str(aluno.user)
        cpf = aluno.user.cpf or ""
        if len(cpf) == 11:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        matricula = aluno.matricula or "—"
        curso_nome = aluno.curso.nome if aluno.curso else "—"
        faculdade = aluno.curso.faculdade.nome if aluno.curso and aluno.curso.faculdade else "—"
        semestre = aluno.semestre_atual() if aluno.semestre_atual() else "—"
        situacao = aluno.get_situacao_display()
        linhas.append([nome, cpf, matricula, curso_nome, faculdade, semestre, situacao])

    return colunas, linhas
