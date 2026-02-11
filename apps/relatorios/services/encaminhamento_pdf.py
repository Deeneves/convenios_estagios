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
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=0.7 * cm,
        bottomMargin=0.7 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="EncTitle",
        parent=styles["Heading1"],
        fontSize=13,
        alignment=1,  # center
        spaceAfter=2,
        textTransform="uppercase",
    )
    sub_style = ParagraphStyle(
        name="EncSub",
        parent=title_style,
        fontSize=11,
        spaceAfter=4,
    )
    bold_style = ParagraphStyle(
        name="Bold",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica-Bold",
    )
    normal_style = ParagraphStyle(
        name="NormalSmall",
        parent=styles["Normal"],
        fontSize=8,
        alignment=4,  # justify
    )

    elements = []
    enc_data = _format_data(enc.data)

    # 1. Título (idêntico ao referência)
    elements.append(Paragraph("ENCAMINHAMENTO DE ESTAGIÁRIOS DE CONTRAPARTIDA - FALS", title_style))
    elements.append(Spacer(1, 0.15 * cm))

    # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[1]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 2. Dados do aluno – tabelas de uma linha com colunas de largura igual para ocupar toda a linha
    _largura_linha = 16 * cm
    _col3 = _largura_linha / 3   # três colunas iguais
    _col2 = _largura_linha / 2   # duas colunas iguais
    _cell_style = ParagraphStyle(
        name="DadosAlunoCell",
        fontSize=8,
        alignment=0,  # LEFT
        spaceAfter=0,
        spaceBefore=0,
        leftIndent=0,
        rightIndent=0,
    )
    _tbl_style = TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])
    matricula_val = aluno.matricula or "—"
    matricula_para = Paragraph(
        f'<b>MATRÍCULA:</b> <font color="#2563EB"><u>{matricula_val}</u></font>',
        _cell_style,
    )
    # Linha 1: MATRÍCULA | RG | CPF
    t1 = Table([
        [matricula_para, Paragraph(f'<b>RG:</b> {aluno.rg or "—"}', _cell_style), Paragraph(f'<b>CPF:</b> {cpf_fmt}', _cell_style)]
    ], colWidths=[_col3, _col3, _col3])
    t1.setStyle(_tbl_style)
    elements.append(t1)

    # Linha 2: NOME | NASCIMENTO | SEXO
    t2 = Table([[
        Paragraph(f'<b>NOME:</b> {nome_completo[:50]}', _cell_style),
        Paragraph(f'<b>NASCIMENTO:</b> {_format_data(aluno.data_nascimento)}', _cell_style),
        Paragraph(f'<b>SEXO:</b> {sexo_display}', _cell_style),
    ]], colWidths=[_col3, _col3, _col3])
    t2.setStyle(_tbl_style)
    elements.append(t2)

    # Linha 3: ENDEREÇO | Nº | CIDADE
    t3 = Table([[
        Paragraph(f'<b>ENDEREÇO:</b> {(aluno.logradouro or "—")[:45]}', _cell_style),
        Paragraph(f'<b>Nº:</b> {aluno.numero or "—"}', _cell_style),
        Paragraph(f'<b>CIDADE:</b> {aluno.cidade or "—"}', _cell_style),
    ]], colWidths=[_col3, _col3, _col3])
    t3.setStyle(_tbl_style)
    elements.append(t3)

    # Linha 4: BAIRRO | COMPLEMENTO | Nº
    t4 = Table([[
        Paragraph(f'<b>BAIRRO:</b> {aluno.bairro or "—"}', _cell_style),
        Paragraph(f'<b>COMPLEMENTO:</b> {(aluno.complemento or "—")[:30]}', _cell_style),
        Paragraph('<b>Nº:</b> ', _cell_style),
    ]], colWidths=[_col3, _col3, _col3])
    t4.setStyle(_tbl_style)
    elements.append(t4)

    # Linha 5: TELEFONE | CELULAR | CEP
    t5 = Table([[
        Paragraph(f'<b>TELEFONE:</b> {aluno.telefone or "—"}', _cell_style),
        Paragraph(f'<b>CELULAR:</b> {aluno.celular or "—"}', _cell_style),
        Paragraph(f'<b>CEP:</b> {_format_cep(aluno.cep)}', _cell_style),
    ]], colWidths=[_col3, _col3, _col3])
    t5.setStyle(_tbl_style)
    elements.append(t5)

    # Linha 6: CURSO | CURSANDO (duas colunas para ocupar toda a linha)
    t6 = Table([[
        Paragraph(f'<b>CURSO:</b> {curso_nome}', _cell_style),
        Paragraph(f'<b>CURSANDO:</b> {ano_cursando}', _cell_style),
    ]], colWidths=[_col2, _col2])
    t6.setStyle(_tbl_style)
    elements.append(t6)
    elements.append(Spacer(1, 0.12 * cm))

     # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[1]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 3. Título da seção de horas e tabela
    elements.append(
        Paragraph(
            "Relatório de Horas Cumpridas pelo(a) Bolsista",
            ParagraphStyle(
                name="H", 
                fontSize=8, 
                fontName="Helvetica-Bold",
                alignment=1  # 1 = TA_CENTER in ReportLab
            ),
        )
    )
    elements.append(Spacer(1, 0.08 * cm))

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
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    elements.append(t_horas)
    elements.append(Spacer(1, 0.35 * cm))

    # 4. Disponibilidade – quadro abaixo da tabela de horas
    _disp_title_style = ParagraphStyle(name="DispTit", fontSize=9, fontName="Helvetica-Bold", alignment=0, spaceAfter=0, spaceBefore=0)
    _disp_line_style = ParagraphStyle(name="DispLine", fontSize=8, alignment=0, spaceAfter=0, spaceBefore=0)
    _disp_horario_style = ParagraphStyle(name="DispHorario", fontSize=8, alignment=2, spaceAfter=0, spaceBefore=0)

    titulo_disp = Paragraph("Dias disponíveis para executar o estágio de contrapartida", _disp_title_style)
    linha1_esq = Paragraph(
        "Disponibilidade: 2ª (  ) 3ª (  ) 4ª (  ) 5ª (  ) 6ª (  ) Todos os dias (  )",
        _disp_line_style,
    )
    linha1_dir = Paragraph("Horário: ___ : ___ a ___ : ___", _disp_horario_style)
    linha2_esq = Paragraph(
        "Disponibilidade: Sáb (  ) Dom (  ) Todos os dias (  )",
        _disp_line_style,
    )
    linha2_dir = Paragraph("Horário: ___ : ___ a ___ : ___", _disp_horario_style)

    tbl_disp = Table(
        [
            [titulo_disp, ""],
            [linha1_esq, linha1_dir],
            [linha2_esq, linha2_dir],
        ],
        colWidths=[10 * cm, 6 * cm],
    )
    tbl_disp.setStyle(
        TableStyle([
            ("SPAN", (0, 0), (1, 0)),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ("LINEBELOW", (0, 1), (-1, 1), 0.5, colors.black),
        ])
    )
    elements.append(tbl_disp)
    elements.append(Spacer(1, 0.08 * cm))
    elements.append(Spacer(1, 0.35 * cm))

    # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[1]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.2 * cm))

    # 5. Declaração
    decl = (
        "Declaro estar ciente da obrigatoriedade e me responsabilizo pelo cumprimento até o final do ano corrente "
        "das horas de contrapartida referente à Bolsa de Estudo - FALS conforme o que dispõe o Decreto Municipal "
        "nº. 4823 de 21 de outubro de 2010 que estabelece 100 horas por ano sob pena de ter o benefício de Bolsa "
        "de Estudos cancelado sem prejuízo das demais sanções previstas no regulamento de contrapartida."
    )
    elements.append(Paragraph(decl, normal_style))
    elements.append(Spacer(1, 1.5 * cm))
    elements.append(Paragraph("Assinatura do Aluno Bolsista", ParagraphStyle(name="Sig", fontSize=8, alignment=1)))
    elements.append(Spacer(1, 0.12 * cm))

    # 6. Texto de encaminhamento
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
    elements.append(Spacer(1, 0.06 * cm))
    elements.append(Paragraph(texto2, normal_style))
    elements.append(Spacer(1, 0.12 * cm))

    # 7. Encaminhamento à : / Em : (duas linhas, assinatura à direita – como no referência)
    dados_enc = [
        [f"Encaminhamento à :", enc.secretaria.nome],
        [f"Em :", enc_data],
        ["", "_________________________"],
        ["", responsavel],
        ["", "RF:"],
    ]
    t_enc = Table(dados_enc, colWidths=[3.2 * cm, 12 * cm])
    t_enc.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(t_enc)
    elements.append(Spacer(1, 0.12 * cm))

    # Linha grossa
    elements.append(Table([[""]], colWidths=[16 * cm], rowHeights=[1]))
    elements[-1].setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.black)]))
    elements.append(Spacer(1, 0.08 * cm))

    # 8. PROTOCOLO DE ENCAMINHAMENTO – estilo: cabeçalho em caixa com bordas grossas; tabela com 3 linhas (label | valor)
    _prot_title_style = ParagraphStyle(
        name="ProtTitle",
        fontSize=11,
        fontName="Helvetica-Bold",
        alignment=1,  # center
        spaceAfter=0,
        spaceBefore=0,
    )
    titulo_prot = Table(
        [[Paragraph("PROTOCOLO DE ENCAMINHAMENTO", _prot_title_style)]],
        colWidths=[16 * cm],
        rowHeights=[0.6 * cm],
    )
    titulo_prot.setStyle(
        TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 2.5, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 2.5, colors.black),
            ("LINELEFT", (0, 0), (-1, 0), 1, colors.black),
            ("LINERIGHT", (0, 0), (-1, 0), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    elements.append(titulo_prot)

    # Tabela do protocolo: 3 linhas – Estagiário(a), Encaminhamento à, Cadastrado em (valor da data em caixa mais estreita)
    _label_w = 3.5 * cm
    _value_wide = 12 * cm
    _value_date = 4 * cm

    dados_prot_1 = [
        ["Estagiário(a):", nome_completo],
        ["Encaminhamento à:", enc.secretaria.nome],
    ]
    t_prot_1 = Table(dados_prot_1, colWidths=[_label_w, _value_wide])
    t_prot_1.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(t_prot_1)

    # Linha Cadastrado em com caixa de data mais estreita
    dados_prot_2 = [["Cadastrado em :", enc_data]]
    t_prot_2 = Table(dados_prot_2, colWidths=[_label_w, _value_date])
    t_prot_2.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(t_prot_2)
    elements.append(Spacer(1, 0.15 * cm))

    # Assinatura protocolo
    elements.append(
        Paragraph(
            f"_________________________<br/>{responsavel}<br/>RF:",
            ParagraphStyle(name="SigProt", fontSize=8, alignment=2),
        )
    )

    doc.build(elements)
    return buffer.getvalue()
