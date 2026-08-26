from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from xml.sax.saxutils import escape


def generate_pdf(name, subject, answers, results, total_score, percentage, grade):
    file_name = f"{name}_Interview_Report.pdf"
    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="AI Technical Interview Report",
        author="Rahul Kumar",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle("ReportTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=22, leading=27, spaceAfter=8)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10, textColor=colors.HexColor("#64748B"), spaceAfter=18)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#1D4ED8"), spaceBefore=12, spaceAfter=7)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.5, leading=14, spaceAfter=7)
    small = ParagraphStyle("Small", parent=body, fontSize=8.5, textColor=colors.HexColor("#475569"))

    story = []
    story.append(Paragraph("AI TECHNICAL INTERVIEW REPORT", title))
    story.append(Paragraph("Professional Interview Assessment", subtitle))

    info = [
        [Paragraph("<b>Candidate</b>", body), Paragraph(escape(str(name)), body)],
        [Paragraph("<b>Subject</b>", body), Paragraph(escape(str(subject)), body)],
        [Paragraph("<b>Questions</b>", body), Paragraph(str(len(answers)), body)],
    ]
    table = Table(info, colWidths=[42 * mm, 120 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EFF6FF")),
        ("BOX", (0,0), (-1,-1), .6, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    summary = [
        [Paragraph("<b>Total Score</b>", body), Paragraph(f"{total_score}", body), Paragraph("<b>Percentage</b>", body), Paragraph(f"{percentage:.2f}%", body), Paragraph("<b>Grade</b>", body), Paragraph(escape(str(grade)), body)]
    ]
    summary_table = Table(summary, colWidths=[27*mm, 22*mm, 27*mm, 24*mm, 22*mm, 22*mm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ("BOX", (0,0), (-1,-1), .6, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#E2E8F0")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)

    story.append(Paragraph("Interview Assessment", heading))
    for i, (answer, result) in enumerate(zip(answers, results), 1):
        story.append(Paragraph(f"Question {i}", heading))
        story.append(Paragraph("<b>Candidate Answer</b>", body))
        story.append(Paragraph(escape(str(answer)).replace("\n", "<br/>"), body))
        story.append(Paragraph("<b>AI Evaluation</b>", body))
        story.append(Paragraph(escape(str(result)).replace("\n", "<br/>"), body))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Developed By", heading))
    story.append(Paragraph("Rahul Kumar", body))
    story.append(Paragraph("Diploma in Computer Science Engineering", small))
    story.append(Paragraph("Govt. Polytechnic Araria", small))

    doc.build(story)
    return file_name
# streamlit run app.py