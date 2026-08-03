from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, HRFlowable

from app.core.config_store import AppConfig

logger = logging.getLogger(__name__)


@dataclass
class ReportSummary:
    period_label: str
    total_activities: int
    km_total: int
    vehicles_involved: int


class _NumberedCanvasMixin:
    def __init__(self, *args, **kwargs):
        from reportlab.pdfgen import canvas
        self._saved_page_states = []
        canvas.Canvas.__init__(self, *args, **kwargs)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count: int):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6b7280"))
        self.drawRightString(A4[0] - 1.5 * cm, 1.0 * cm,
            f"Pagina {self._pageNumber} de {page_count}  |  MADEMAXI - Todos os direitos reservados")


def _make_canvas():
    from reportlab.pdfgen import canvas
    class NumberedCanvas(_NumberedCanvasMixin, canvas.Canvas):
        pass
    return NumberedCanvas


def _fmt_dt(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y %H:%M")
    s = str(value)
    if "T" in s:
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            pass
    return s[:16]


def _get_logo_path(config: AppConfig) -> Path | None:
    """Retorna o caminho do logo: config primeiro, depois fallback padrao."""
    if config.logo_path:
        p = Path(config.logo_path)
        if p.exists():
            return p
    fallback = Path(__file__).parent.parent / "assets" / "logo_mademaxi.png"
    if fallback.exists():
        return fallback
    return None


class ReportService:
    def generate_pdf(
        self,
        *,
        output_path: Path,
        config: AppConfig,
        summary: ReportSummary,
        rows: List[Tuple[dict, dict]],
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "MademaxiTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=2,
            fontName="Helvetica-Bold",
            alignment=1,
        )
        subtitle_style = ParagraphStyle(
            "MademaxiSubtitle",
            parent=styles["BodyText"],
            fontSize=10,
            textColor=colors.HexColor("#6b7280"),
            spaceAfter=14,
            alignment=1,
        )
        section_style = ParagraphStyle(
            "MademaxiSection",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#E53935"),
            spaceAfter=12,
            fontName="Helvetica-Bold",
        )
        metric_label = ParagraphStyle(
            "MetricLabel",
            parent=styles["BodyText"],
            fontSize=9,
            textColor=colors.HexColor("#6b7280"),
            alignment=1,
        )
        metric_value = ParagraphStyle(
            "MetricValue",
            parent=styles["BodyText"],
            fontSize=20,
            textColor=colors.HexColor("#1a1a1a"),
            fontName="Helvetica-Bold",
            alignment=1,
        )
        small = ParagraphStyle(
            "small", parent=styles["BodyText"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563")
        )

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=2.2 * cm,
            bottomMargin=1.6 * cm,
            title="Relatorio de Atividades de Veiculos - MADEMAXI",
        )

        story = []

        # === CABECALHO CENTRALIZADO COM LOGO ===
        logo_path = _get_logo_path(config)
        logo_cell = ""
        if logo_path:
            try:
                img = Image(str(logo_path), width=2.8 * cm, height=2.8 * cm)
                logo_cell = img
            except Exception:
                logger.exception("Falha ao carregar logo: %s", logo_path)

        company_name = config.company_name or "MADEMAXI - Materiais de Construcao e Ferragem"
        header_inner = Table(
            [[logo_cell], [Paragraph(f"<b>{company_name}</b>", title_style)]],
            colWidths=[None],
            hAlign="CENTER",
        )
        header_inner.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("BOTTOMPADDING", (0, 0), (0, 0), 6),
            ("TOPPADDING", (0, 1), (0, 1), 2),
            ("BOTTOMPADDING", (0, 1), (0, 1), 0),
        ]))

        header_outer = Table([[header_inner]], colWidths=[A4[0] - 3 * cm], hAlign="CENTER")
        header_outer.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(header_outer)

        story.append(Paragraph("Relatorio de Atividades de Veiculos", subtitle_style))

        story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#E53935"), spaceAfter=14))

        story.append(Paragraph(
            f"<b>Periodo:</b> {summary.period_label} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Gerado em:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            subtitle_style,
        ))
        story.append(Spacer(1, 0.2 * cm))

        # === RESUMO EM CARDS ===
        story.append(Paragraph("Resumo do Periodo", section_style))

        avg = round(summary.km_total / summary.vehicles_involved, 1) if summary.vehicles_involved > 0 else 0
        resumo_data = [
            [
                Paragraph("TOTAL DE<br/>ATIVIDADES", metric_label),
                Paragraph("QUANTIDADE<br/>TOTAL", metric_label),
                Paragraph("VEICULOS<br/>ENVOLVIDOS", metric_label),
                Paragraph("MEDIA POR<br/>VEICULO", metric_label),
            ],
            [
                Paragraph(str(summary.total_activities), metric_value),
                Paragraph(str(summary.km_total), metric_value),
                Paragraph(str(summary.vehicles_involved), metric_value),
                Paragraph(str(avg), metric_value),
            ],
        ]
        resumo_table = Table(resumo_data, colWidths=[4.0 * cm] * 4, hAlign="CENTER")
        resumo_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
            ("LINEBELOW", (0, 0), (-1, 0), 2, colors.HexColor("#E53935")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(resumo_table)
        story.append(Spacer(1, 0.5 * cm))

        # === TABELA DETALHADA ===
        story.append(Paragraph("Atividades Detalhadas", section_style))

        data = [
            ["Data/Hora", "Placa", "Modelo", "Categoria", "Qtd", "Observacoes"]
        ]

        for a, v in rows:
            data.append(
                [
                    _fmt_dt(a.get("data_hora")),
                    v.get("placa", ""),
                    v.get("modelo") or "",
                    v.get("categoria") or "",
                    str(a.get("quantidade") or 0),
                    (a.get("observacoes") or "")[:60],
                ]
            )

        table = Table(
            data,
            repeatRows=1,
            colWidths=[3.0 * cm, 2.0 * cm, 3.2 * cm, 2.4 * cm, 1.4 * cm, 5.8 * cm],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a1a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e5e7eb")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (5, 1), (5, -1), "LEFT"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LINEBELOW", (0, 0), (-1, 0), 2.5, colors.HexColor("#E53935")),
                ]
            )
        )
        story.append(table)

        story.append(Spacer(1, 0.6 * cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db"), spaceAfter=6))
        story.append(Paragraph(
            f"<font size=8 color=#9ca3af>Este relatorio foi gerado automaticamente pelo sistema MADEMAXI. "
            f"Para duvidas, entre em contato com o departamento de logistica.</font>",
            small,
        ))

        doc.build(story, canvasmaker=_make_canvas())
        logger.info("PDF gerado: %s", output_path)
