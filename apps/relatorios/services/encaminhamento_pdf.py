"""Geração do PDF de encaminhamento conforme template oficial FALS."""

from datetime import timedelta
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from core.utils.formatters import format_cpf


def _format_cep(value):
    """Formata CEP: 11720010 -> 11.720-010"""
    if not value:
        return ""
    digits = "".join(c for c in str(value) if c.isdigit())
    if len(digits) != 8:
        return value
    return f"{digits[:2]}.{digits[2:5]}-{digits[5:]}"


def _format_data(data):
    """Formata data para dd/mm/yyyy"""
    if not data:
        return ""
    return data.strftime("%d/%m/%Y")


def _format_horas_minutos(td: timedelta):
    """Formata duração como HH:MM (ex: 125:00)"""
    if not td:
        return "00:00"
    total = int(td.total_seconds())
    h = total // 3600
    m = (total % 3600) // 60
    return f"{h}:{m:02d}"


def _horas_por_ano(aluno):
    """Retorna dict {1: timedelta, 2: timedelta, ...} e total, média."""
    from apps.contrapartida.models import Horas

    if not aluno.data_ingresso:
        return {1: timedelta(0), 2: timedelta(0), 3: timedelta(0), 4: timedelta(0)}, timedelta(0), timedelta(0)

    horas_qs = Horas.objects.filter(aluno=aluno).only("data_registro", "quantidade")
    ano_map = {1: timedelta(0), 2: timedelta(0), 3: timedelta(0), 4: timedelta(0)}
    ingresso = aluno.data_ingresso

    for h in horas_qs:
        data_reg = h.data_registro
        qtd = h.quantidade
        if not qtd:
            continue
        # Ano do curso = anos desde ingresso (1-based)
        anos_diff = (data_reg.year - ingresso.year) + (
            1 if (data_reg.month, data_reg.day) >= (ingresso.month, ingresso.day) else 0
        )
        ano_curso = min(max(anos_diff, 1), 4)
        ano_map[ano_curso] = ano_map[ano_curso] + qtd

    total = ano_map[1] + ano_map[2] + ano_map[3] + ano_map[4]
    count = sum(1 for v in ano_map.values() if v and v.total_seconds() > 0)
    media_sec = total.total_seconds() / count if count > 0 else 0
    media = timedelta(seconds=int(media_sec))

    return ano_map, total, media


def gerar_pdf_encaminhamento(encaminhamento):
    """Gera PDF do encaminhamento no formato do template oficial."""
    enc = encaminhamento
    aluno = enc.aluno
    user = aluno.user
    curso = aluno.curso

    nome_completo = f"{user.first_name or ''} {user.last_name or ''}".strip() or str(user)
    cpf_fmt = format_cpf(user.cpf) if user.cpf else ""
    responsavel = f"{enc.responsavel_emissao.first_name or ''} {enc.responsavel_emissao.last_name or ''}".strip()
    responsavel = responsavel or str(enc.responsavel_emissao)

    ano_map, total_horas, media_horas = _horas_por_ano(aluno)
    h1 = _format_horas_minutos(ano_map.get(1))
    h2 = _format_horas_minutos(ano_map.get(2))
    h3 = _format_horas_minutos(ano_map.get(3))
    h4 = _format_horas_minutos(ano_map.get(4))
    h_total = _format_horas_minutos(total_horas)
    h_media = _format_horas_minutos(media_horas)

    semestre = aluno.semestre_atual()
    ano_cursando = f"{(semestre + 1) // 2}º ANO" if semestre else "—"
    curso_nome = curso.nome if curso else "—"
    bolsista_desde = _format_data(aluno.data_ingresso) if aluno.data_ingresso else "—"
    sexo_display = aluno.get_sexo_display() if aluno.sexo else "—"

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="EncTitle",
        parent=styles["Heading1"],
        fontSize=14,
        alignment=1,  # center
        spaceAfter=6,
        textTransform="uppercase",
    )
    sub_style = ParagraphStyle(
        name="EncSub",
        parent=title_style,
        fontSize=12,
        spaceAfter=8,
    )
    bold_style = ParagraphStyle(
        name="Bold",
        parent=styles["Normal"],
        fontSize=9,
        fontName="Helvetica-Bold",
    )
    normal_style = ParagraphStyle(
        name="NormalSmall",
        parent=styles["Normal"],
        fontSize=9,
        alignment=4,  # justify
    )

    elements = []

    # 1. Título
    elements.append(Paragraph("ENCAMINHAMENTO DE ESTAGIÁRIOS", title_style))
    elements.append(Paragraph("DE CONTRAPARTIDA - FALS", sub_style))
    elements.append(Spacer(1, 0.3 * cm))

    # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[2]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.4 * cm))

    # 2. Dados do aluno (layout em grid - 2 pares label/valor por linha)
    dados_aluno = [
        ["MATRÍCULA:", aluno.matricula or "—", "NOME:", nome_completo[:50]],
        ["NASCIMENTO:", _format_data(aluno.data_nascimento), "SEXO:", sexo_display],
        ["ENDEREÇO:", (aluno.logradouro or "—")[:35], "Nº:", aluno.numero or "—"],
        ["CIDADE:", aluno.cidade or "—", "BAIRRO:", aluno.bairro or "—"],
        ["COMPLEMENTO:", aluno.complemento or "—", "Nº:", ""],
        ["TELEFONE:", aluno.telefone or "—", "CELULAR:", aluno.celular or "—"],
        ["RG:", aluno.rg or "—", "CPF:", cpf_fmt],
        ["CEP:", _format_cep(aluno.cep), "", ""],
    ]
    t_aluno = Table(dados_aluno, colWidths=[2.2 * cm, 4.8 * cm, 1.8 * cm, 6 * cm])
    t_aluno.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.HexColor("#2563EB")),  # Matrícula em azul
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    elements.append(t_aluno)
    elements.append(Spacer(1, 0.3 * cm))

    # Linha fina
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[0.5]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.3 * cm))

    # 3. Curso e bolsista
    dados_curso = [
        ["CURSO:", curso_nome, "CURSANDO:", ano_cursando, "BOLSISTA DESDE:", bolsista_desde],
    ]
    t_curso = Table(dados_curso, colWidths=[1.5 * cm, 5 * cm, 2 * cm, 2 * cm, 2.5 * cm, 2.5 * cm])
    t_curso.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTNAME", (4, 0), (4, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(t_curso)
    elements.append(Spacer(1, 0.2 * cm))

    # 4. Tabela de horas
    titulo_horas = Paragraph(
        "<b>Relatório de Horas Cumpridas pelo(a) Bolsista</b>",
        ParagraphStyle(name="H", fontSize=9, fontName="Helvetica-Bold"),
    )
    elements.append(titulo_horas)
    elements.append(Spacer(1, 0.1 * cm))

    dados_horas = [
        ["Ano", "1º ANO", "2º ANO", "3º ANO", "4º ANO", "TOTAL", "MÉDIA"],
        ["Qtd. Horas", h1, h2, h3, h4, h_total, h_media],
    ]
    t_horas = Table(
        dados_horas,
        colWidths=[2.2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm],
    )
    t_horas.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, 1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 1), (0, 1), colors.HexColor("#CC0000")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(t_horas)
    elements.append(Spacer(1, 0.3 * cm))

    # Linha fina
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[0.5]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 5. Disponibilidade
    disp = Paragraph(
        "<b>Dias disponíveis para executar o estágio de contrapartida</b><br/>"
        "Disponibilidade: 2ª (  ) 3ª (  ) 4ª (  ) 5ª (  ) 6ª (  ) Todos os dias (  ) Horário: ___ : ___ a ___ : ___<br/>"
        "Disponibilidade: Sáb (  ) Dom (  ) Todos os dias (  ) Horário: ___ : ___ a ___ : ___",
        ParagraphStyle(name="Disp", fontSize=9, fontName="Helvetica-Bold"),
    )
    elements.append(disp)
    elements.append(Spacer(1, 0.3 * cm))

    # Linha fina
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[0.5]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 6. Declaração
    decl = (
        "Declaro estar ciente da obrigatoriedade e me responsabilizo pelo cumprimento até o final do ano corrente "
        "das horas de contrapartida referente à Bolsa de Estudo - FALS conforme o que dispõe o Decreto Municipal "
        "nº. 4823 de 21 de outubro de 2010 que estabelece 100 horas por ano sob pena de ter o benefício de Bolsa "
        "de Estudos cancelado sem prejuízo das demais sanções previstas no regulamento de contrapartida."
    )
    elements.append(Paragraph(decl, normal_style))
    elements.append(Spacer(1, 0.1 * cm))
    elements.append(Paragraph("_________________________ Assinatura do Aluno Bolsista", ParagraphStyle(name="Sig", fontSize=9, alignment=1)))
    elements.append(Spacer(1, 0.3 * cm))

    # Linha fina
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[0.5]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 7. Texto de encaminhamento
    texto1 = (
        "Encaminhamos o(a) aluno(a) supra citado(a) para cumprir horas de contrapartida da Bolsa de Estudos - FALS "
        "nesta Secretaria, a partir desta data, uma vez que esta Municipalidade deve ofertar oportunidades para que "
        "este aluno(a) possa cumprir suas respectivas horas conforme Convênio firmado com a instituição FALS e "
        "regulamentado pelo Decreto nº. 4823 de 21 de outubro de 2010."
    )
    texto2 = (
        "Solicitamos a V.Sa., que os relatórios de horas e atividades desenvolvidas sejam encaminhados devidamente "
        "preenchidos e assinados pelo aluno bolsista e a chefia imediata, com a devida ciência do titular da pasta "
        "conforme Memos Circulares Sead nº. 129/10, 264/11 e 302/11 ao término do estágio."
    )
    elements.append(Paragraph(texto1, normal_style))
    elements.append(Spacer(1, 0.15 * cm))
    elements.append(Paragraph(texto2, normal_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Encaminhamento à / Em / Assinatura (layout: esq = Enc à, dir = Em + assinatura)
    enc_data = _format_data(enc.data)
    dados_enc = [
        [f"Encaminhamento à: {enc.secretaria.nome}", f"Em: {enc_data}"],
        ["", ""],
        ["", "_________________________"],
        ["", responsavel],
        ["", "RF:"],
    ]
    t_enc = Table(dados_enc, colWidths=[10 * cm, 5.5 * cm])
    t_enc.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    elements.append(t_enc)
    elements.append(Spacer(1, 0.3 * cm))

    # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[2]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.15 * cm))

    # 8. PROTOCOLO DE ENCAMINHAMENTO
    elements.append(
        Paragraph(
            "PROTOCOLO DE ENCAMINHAMENTO",
            ParagraphStyle(name="Prot", fontSize=11, fontName="Helvetica-Bold", alignment=1),
        )
    )
    elements.append(Spacer(1, 0.1 * cm))

    # Linha fina
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[0.5]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    dados_prot = [
        ["Estagiário(a):", nome_completo],
        ["Encaminhamento à:", enc.secretaria.nome],
        ["Cadastrado em:", enc_data],
    ]
    t_prot = Table(dados_prot, colWidths=[3.5 * cm, 11 * cm])
    t_prot.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(t_prot)
    elements.append(Spacer(1, 0.2 * cm))

    # Assinatura protocolo
    elements.append(
        Paragraph(
            f"_________________________<br/>{responsavel}<br/>RF:",
            ParagraphStyle(name="SigProt", fontSize=9, alignment=2),
        )
    )

    doc.build(elements)
    return buffer.getvalue()
