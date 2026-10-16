
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    LongTable, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.enums import TA_LEFT


def generate_pdf_report(summary, feedback_data, complaint_summary, ai_summary):
    report_date = datetime.now()
    date_filename = report_date.strftime("%Y-%m-%d")
    date_display = report_date.strftime("%B %d, %Y")
    # 1. Create PDF document
    doc = SimpleDocTemplate(
        f"Customer_Feedback_Report_{date_filename}.pdf",
        pagesize=landscape(A4),
        leftMargin=35,
        rightMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    elements = []
    styles = getSampleStyleSheet()

    # 2. Report title
    title = Paragraph(
        "Customer Feedback Analysis - Weekly Report",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 15))
    elements.append(
        Paragraph(f"Generated: {date_display}", styles["Normal"])
    )
    # 3. Executive summary
    elements.append(
        Paragraph("Executive Summary", styles["Heading2"])
    )
    elements.append(Spacer(1, 10))

    summary_data = [
        ["Feedback Records", "Products with Issues", "Average Rating"],
        [
            str(len(feedback_data)),
            str(len(complaint_summary)),
            f'{summary["average_rating"]:.2f} / 5'
        ],
        ["Recommendation Rate", "Product Issues", "Contact Requests"],
        [
            f'{summary["recommendation_rate"]:.1f}%',
            str(summary["product_issues"]),
            str(summary["contact_requests"])
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[180, 180, 180],
        rowHeights=[25, 40, 25, 40]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTSIZE", (0, 1), (-1, 1), 16),
        ("FONTSIZE", (0, 3), (-1, 3), 16),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, colors.lightgrey),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    # AI-generated executive summary
    elements.append(
        Paragraph("AI Management Analysis", styles["Heading2"])
    )

    elements.append(Spacer(1, 8))

    ai_style = ParagraphStyle(
        "AIAnalysis",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=12
    )

    for paragraph in ai_summary.split("\n"):
        if paragraph.strip():
            elements.append(
                Paragraph(escape(paragraph), ai_style)
            )

    elements.append(Spacer(1, 15))

    # 4. Product issues
    elements.append(
        Paragraph("Product Issues - By Severity", styles["Heading2"])
    )
    elements.append(Spacer(1, 10))

    # Style for wrapped table text
    cell_style = ParagraphStyle(
        "IssueCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT
    )

    header_style = ParagraphStyle(
        "IssueHeader",
        parent=cell_style,
        fontName="Helvetica-Bold"
    )

    headers = [
        "Product", "Category", "Comment",
        "Issue", "Severity", "Suggested Action"
    ]

    issue_data = [
        [Paragraph(h, header_style) for h in headers]
    ]

    # Collect all product issues
    issues = []

    for row in feedback_data:
        if row["Feedback type"] == "Product issue":

            product = row["Product"]
            comment = row["Comment"]

            # Import here to avoid circular import at module load
            from main import analyze_issue_comment
            analysis = analyze_issue_comment(product, comment)

            issues.append({
                "product": product,
                "category": analysis["issue_category"],
                "comment": comment,
                "issue": analysis["summary"],
                "severity": analysis["severity"],
                "action": analysis["suggested_action"]
            })

    # Sort from High to Low severity
    severity_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    issues.sort(
        key=lambda x: severity_order.get(x["severity"], 3)
    )

    # Build table rows
    for issue in issues:
        values = [
            issue["product"],
            issue["category"],
            issue["comment"],
            issue["issue"],
            issue["severity"],
            issue["action"]
        ]

        issue_data.append([
            Paragraph(escape(str(value)), cell_style)
            for value in values
        ])

    # 5. Create product issues table
    issue_table = LongTable(
        issue_data,
        colWidths=[90, 100, 190, 120, 60, 170],
        repeatRows=1,
        hAlign="LEFT"
    )

    issue_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.whitesmoke]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.grey),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.lightgrey),
    ]))

    elements.append(issue_table)
    # 7. Analyze customer feedback themes
    from main import summarize_feedback_themes

    # 7. Customer suggestions and compliments
    for section_title, feedback_type, text_column in [
        ("Customer Suggestions", "Suggestion", "Improvement suggestion"),
        ("Customer Compliments", "Compliment", "Comment")
    ]:
        elements.append(Spacer(1, 20))
        elements.append(
            Paragraph(section_title, styles["Heading2"])
        )
        elements.append(Spacer(1, 10))
        theme_counts = summarize_feedback_themes(
            feedback_data, feedback_type
        )

        if theme_counts:
            theme_text = ", ".join(
                f"{theme} ({count})"
                for theme, count in theme_counts.items()
            )

            elements.append(
                Paragraph(
                    f"<b>Key themes:</b> {theme_text}",
                    styles["Normal"]
                )
            )
            elements.append(Spacer(1, 12))
            # Generate a short management interpretation
            top_count = max(theme_counts.values())

            top_themes = [
                theme for theme, count in theme_counts.items()
                if count == top_count
            ]

            if len(top_themes) == 1:
                interpretation = (
                    f"The most frequently identified theme is "
                    f"{top_themes[0].lower()}, with {top_count} mentions."
                )
            else:
                interpretation = (
                    f"The most frequently identified themes are "
                    f"{' and '.join(top_themes).lower()}, "
                    f"with {top_count} mentions each."
                )

            elements.append(
                Paragraph(
                    f"<b>Analysis:</b> {interpretation}",
                    styles["Normal"]
                )
            )
            elements.append(Spacer(1, 12))
        section_data = [[
            Paragraph("Product", header_style),
            Paragraph("Customer Feedback", header_style)
        ]]

        for row in feedback_data:
            if row["Feedback type"] == feedback_type:
                section_data.append([
                    Paragraph(escape(row["Product"] or ""), cell_style),
                    Paragraph(escape(row[text_column] or ""), cell_style)
                ])

        if len(section_data) == 1:
            section_data.append([
                Paragraph("No records", cell_style),
                Paragraph("", cell_style)
            ])

        section_table = LongTable(
            section_data,
            colWidths=[150, 580],
            repeatRows=1,
            hAlign="LEFT"
        )

        section_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.whitesmoke]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.grey),
            ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.lightgrey),
        ]))

        elements.append(section_table)

    # 6. Generate PDF
    doc.build(elements)
