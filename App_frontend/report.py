from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def create_report(

    prediction,
    risk,
    wellness_score,
    driver,
    analytics

):

    pdf = "Stress_Report.pdf"

    doc = SimpleDocTemplate(

        pdf,

        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=25

    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    story = []

    
    # HEADER
    

    story.append(

        Paragraph(
            "🧠 Stress SensAI",
            title
        )

    )

    story.append(

        Paragraph(
            "<b>Personalized Stress Intelligence Platform</b>",
            normal
        )

    )

    story.append(

        Spacer(
            1,
            .35*inch
        )

    )

    
    # SUMMARY
    

    story.append(

        Paragraph(
            "Prediction Summary",
            heading
        )

    )

    summary = [

        [

            "Prediction",

            f"{prediction:.2f}"

        ],

        [

            "Risk",

            risk

        ],

        [

            "Wellness Score",

            f"{wellness_score}/100"

        ],

        [

            "Primary Driver",

            driver["title"]

        ]

    ]

    table = Table(

        summary,

        colWidths=[180,250]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E6F4EA")),

            ("BACKGROUND",(1,0),(1,-1),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold")

        ])

    )

    story.append(table)

    story.append(

        Spacer(

            1,

            .25*inch

        )

    )

    
    # RECOMMENDATION
    

    story.append(

        Paragraph(
            "AI Recommendation",
            heading
        )
    )

    story.append(

        Paragraph(
            driver["description"],
            normal
        )
    )

    story.append(

        Spacer(
            1,
            8
        )
    )

    story.append(

        Paragraph(
            f"<b>Suggested Action</b><br/>{driver['action']}",
            normal
        )

    )

    story.append(

        Spacer(
            1,
            8
        )
    )

    story.append(

        Paragraph(
            f"<b>Expected Benefit</b><br/>{driver['benefit']}",
            normal
        )

    )

    story.append(

        Spacer(
            1,
            .25*inch
        )
    )

    
    # ANALYTICS
    

    story.append(

        Paragraph(
            "Analytics Summary",
            heading
        )
    )

    analytics_table = [

        [

            "Current",

            analytics["current"]

        ],

        [

            "Average",

            analytics["average"]

        ],

        [

            "Highest",

            analytics["highest"]

        ],

        [

            "Lowest",

            analytics["lowest"]

        ],

        [

            "Total Predictions",

            analytics["total_predictions"]

        ]

    ]

    table2 = Table(

        analytics_table,

        colWidths=[180,250]

    )

    table2.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DBEAFE")),

            ("BACKGROUND",(1,0),(1,-1),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold")

        ])

    )

    story.append(table2)

    story.append(

        Spacer(

            1,

            .25*inch

        )

    )

    
    # WELLNESS INTERPRETATION
    

    story.append(

        Paragraph(

            "Wellness Interpretation",

            heading

        )

    )

    if wellness_score >= 80:

        msg = "Excellent wellness. Your recent behavioural pattern indicates healthy stress management."

    elif wellness_score >= 60:

        msg = "Good wellness. Small lifestyle improvements may further reduce your stress."

    elif wellness_score >= 40:

        msg = "Moderate wellness. Follow the personalized recommendations regularly."

    else:

        msg = "High stress detected. Consider improving your daily habits and consult a healthcare professional if stress persists."

    story.append(

        Paragraph(

            msg,

            normal

        )

    )

    story.append(

        Spacer(

            1,

            .25*inch

        )

    )

    
    # DISCLAIMER
    

    story.append(

        Paragraph(

            "Disclaimer",

            heading

        )

    )

    story.append(

        Paragraph(

            "Stress SensAI provides AI-assisted wellness insights based on behavioural information. "
            "It is intended for educational purposes only and should not be considered a medical diagnosis. "
            "Always consult a qualified healthcare professional for medical advice.",

            normal

        )

    )

    story.append(

        Spacer(

            1,

            .25*inch

        )

    )

    
    # FOOTER
    

    story.append(

        Paragraph(

            "<font color='grey'><i>Generated automatically by Stress SensAI • AI Powered Personalized Stress Intelligence Platform</i></font>",

            normal

        )

    )

    doc.build(

        story

    )

    return pdf