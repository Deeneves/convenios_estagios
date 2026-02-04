"""Helpers para geração de relatórios em PDF usando reportlab."""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def gerar_pdf_tabela(titulo, colunas, linhas, orientacao="portrait"):
    """
    Gera um PDF com uma tabela.

    Args:
        titulo: Título do relatório
        colunas: Lista de nomes das colunas
        linhas: Lista de listas (cada lista é uma linha)
        orientacao: "portrait" ou "landscape"

    Returns:
        bytes: Conteúdo do PDF
    """
    buffer = BytesIO()
    pagesize = A4
    if orientacao == "landscape":
        pagesize = (A4[1], A4[0])

    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=12,
    )

    elements = []
    elements.append(Paragraph(titulo, title_style))
    elements.append(Spacer(1, 0.5 * cm))

    dados = [colunas] + linhas
    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
            ]
        )
    )
    elements.append(tabela)

    doc.build(elements)
    return buffer.getvalue()


def gerar_pdf_documento(titulo, campos):
    """
    Gera um PDF no formato de documento (lista de campo: valor).

    Args:
        titulo: Título do documento
        campos: Lista de tuplas (label, valor)

    Returns:
        bytes: Conteúdo do PDF
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="DocTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=14,
    )

    elements = [Paragraph(titulo, title_style), Spacer(1, 0.5 * cm)]

    dados = [[str(label), str(valor or "—")] for label, valor in campos]
    tabela = Table(dados, colWidths=[5 * cm, 10 * cm])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(tabela)
    doc.build(elements)
    return buffer.getvalue()
