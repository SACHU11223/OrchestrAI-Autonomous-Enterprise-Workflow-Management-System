"""
OrchestrAI - PDF Service
Generates PDF reports using reportlab.
"""
import io
import json
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def generate_report_pdf(report_data: dict) -> bytes:
    """Generate a PDF report from report data."""
    if not HAS_REPORTLAB:
        return _generate_simple_pdf(report_data)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"],
        fontSize=24, textColor=HexColor("#667eea"),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading2"],
        fontSize=16, textColor=HexColor("#00d4ff"),
        spaceAfter=10, spaceBefore=15
    )
    body_style = ParagraphStyle(
        "CustomBody", parent=styles["Normal"],
        fontSize=11, spaceAfter=8, leading=16
    )

    elements = []

    # Title
    title = report_data.get("title", "OrchestrAI Report")
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
    elements.append(Spacer(1, 20))

    # Executive Summary
    content = report_data.get("content", report_data)
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except:
            content = {"summary": content}

    summary = content.get("executive_summary", report_data.get("summary", ""))
    if summary:
        elements.append(Paragraph("Executive Summary", heading_style))
        elements.append(Paragraph(summary, body_style))
        elements.append(Spacer(1, 10))

    # Metrics
    metrics = content.get("metrics", {})
    if metrics:
        elements.append(Paragraph("Key Metrics", heading_style))
        metric_data = [[k.replace("_", " ").title(), str(v)] for k, v in metrics.items()]
        if metric_data:
            table = Table(metric_data, colWidths=[3 * inch, 2 * inch])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#131738")),
                ("TEXTCOLOR", (0, 0), (-1, -1), HexColor("#ffffff")),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#667eea")),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 15))

    # Highlights
    for section in ["highlights", "concerns", "recommendations"]:
        items = content.get(section, [])
        if items:
            elements.append(Paragraph(section.title(), heading_style))
            for item in items:
                elements.append(Paragraph(f"• {item}", body_style))
            elements.append(Spacer(1, 10))

    doc.build(elements)
    return buffer.getvalue()


def _generate_simple_pdf(report_data: dict) -> bytes:
    """Generate a simple text-based fallback when reportlab is not available."""
    content = json.dumps(report_data, indent=2, default=str)
    header = f"OrchestrAI Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*60}\n\n"
    return (header + content).encode("utf-8")
