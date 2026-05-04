from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

def create_report():
    pdf_filename = "Investigation_Report_20234029.pdf"
    output_path = os.path.join(r"e:\Last Year\AI for cyber scurity\AI_Project", pdf_filename)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    dark_navy = colors.HexColor("#1a1a2e")
    red_alert = colors.HexColor("#e63946")
    
    styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, spaceAfter=24, textColor=dark_navy, alignment=1))
    styles.add(ParagraphStyle(name='CoverText', parent=styles['Normal'], fontName='Helvetica', fontSize=14, spaceAfter=12, alignment=1))
    styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=16, spaceAfter=12, textColor=dark_navy))
    styles.add(ParagraphStyle(name='SubHeader', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=12, spaceAfter=8, textColor=dark_navy))
    styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], fontName='Helvetica', fontSize=11, spaceAfter=8, leading=14))
    styles.add(ParagraphStyle(name='AlertText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, spaceAfter=8, leading=14, textColor=red_alert))
    styles.add(ParagraphStyle(name='BulletItem', parent=styles['Normal'], fontName='Helvetica', fontSize=11, spaceAfter=6, leading=14, leftIndent=20, bulletIndent=10))

    Story = []

    # Cover Page
    Story.append(Spacer(1, 2*inch))
    Story.append(Paragraph("SOC Investigation Report: Slow & Low IoT DDoS Evasion", styles['CoverTitle']))
    Story.append(Spacer(1, 1*inch))
    Story.append(Paragraph("Course: AI for Cybersecurity — CSA412", styles['CoverText']))
    Story.append(Paragraph("University: Future University in Egypt", styles['CoverText']))
    Story.append(Paragraph("Student ID: 20234029", styles['CoverText']))
    Story.append(Paragraph("Date: 2026-04-27", styles['CoverText']))
    Story.append(PageBreak())

    # Section 1 — Executive Summary
    Story.append(Paragraph("Section 1 — Executive Summary", styles['SectionHeader']))
    Story.append(Paragraph("This report details the investigation of a sophisticated 'Slow & Low' DDoS attack orchestrated by a botnet. Unlike traditional volumetric DDoS attacks that attempt to overwhelm the target with sheer traffic volume, a Slow & Low attack operates below standard detection thresholds. It deliberately sends requests at a minimal rate and keeps connections open for extended periods, effectively exhausting server resources (like connection pools) without triggering standard rate-limiting alarms.", styles['NormalText']))
    Story.append(Paragraph("The scenario represents a critical danger to modern infrastructure, particularly IoT environments, because standard rule-based Intrusion Detection Systems (IDS) often fail to detect such evasion tactics, leading to silent service degradation or outages.", styles['NormalText']))
    Story.append(Spacer(1, 0.2*inch))

    # Section 2 — Attack Vector Summary (Red Team Analysis)
    Story.append(Paragraph("Section 2 — Attack Vector Summary (Red Team Analysis)", styles['SectionHeader']))
    Story.append(Paragraph("The attack leverages the 'Slow & Low' DDoS concept, which establishes multiple connections and trickles data to hold them open as long as possible.", styles['NormalText']))
    Story.append(Paragraph("• <b>Attack Rate Formula:</b> (20223617 % 100) / 100 = 0.17 pkts/sec", styles['BulletItem']))
    Story.append(Paragraph("• <b>Multi-phase Structure:</b> Probe (0-20%) → Sustain (20-80%) → Cool (80-100%)", styles['BulletItem']))
    Story.append(Paragraph("• <b>Botnet:</b> 8 devices distributed across 3 subnets.", styles['BulletItem']))
    Story.append(Paragraph("• <b>Slowloris Traits:</b> Small TCP window sizes (512-1024 bytes) and long flow durations (8-15s).", styles['BulletItem']))
    Story.append(Paragraph("• <b>Why it evades traditional IDS thresholds:</b> By maintaining a minimal packet rate and blending in with normal traffic, the attack avoids volumetric triggers and rate-limiters entirely.", styles['AlertText']))
    Story.append(Spacer(1, 0.2*inch))

    # Section 3 — Blue Team ML Model Evaluation
    Story.append(Paragraph("Section 3 — Blue Team ML Model Evaluation", styles['SectionHeader']))
    Story.append(Paragraph("To counter the evasion tactics, Machine Learning models were deployed to analyze flow features.", styles['NormalText']))
    
    # Table for ML Comparison
    data = [
        ['Metric', 'Random Forest', 'Logistic Regression'],
        ['Accuracy', '> 99%', '~ 95%'],
        ['Precision', '> 99%', '-'],
        ['Recall', '> 99%', '~ 90%'],
        ['F1-Score', '> 99%', '~ 91%']
    ]
    
    t = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 0.2*inch))
    Story.append(Paragraph("The Random Forest classifier outperformed Logistic Regression significantly. Crucially, the <b>Feature Importance</b> analysis revealed that the top features contributing to detection were <i>rolling_rate_mean</i>, <i>flow_density_30s</i>, and <i>inter_arrival_time</i>. These temporal features capture the sustained, low-intensity nature of the attack.", styles['NormalText']))
    Story.append(Spacer(1, 0.2*inch))

    # Section 4 — Rule-Based vs AI Comparison
    Story.append(Paragraph("Section 4 — Rule-Based vs AI Comparison", styles['SectionHeader']))
    Story.append(Paragraph("A Rule-Based IDS set at a threshold of 5.0 pkts/s yielded a Recall of ≈ 0%. This is a complete failure to detect the threat.", styles['AlertText']))
    Story.append(Paragraph("<b>Why Rule-Based Fails:</b> The attack was engineered to run at 0.17 pkts/sec. Hardcoded threshold rules only flag volumetric anomalies. The IDS never triggers because the traffic blends in with normal behavior.", styles['NormalText']))
    Story.append(Paragraph("<b>Why AI was Necessary:</b> AI models, utilizing rolling windows and time-series feature engineering, evaluate the <i>behavior</i> of the flow over time. This behavioral analysis is essential for identifying Slow & Low attacks.", styles['NormalText']))
    Story.append(Spacer(1, 0.2*inch))

    # Section 5 — Attacks That Bypassed AI
    Story.append(Paragraph("Section 5 — Attacks That Bypassed AI", styles['SectionHeader']))
    Story.append(Paragraph("While the AI models achieved excellent overall performance, certain edge cases still bypassed detection:", styles['NormalText']))
    Story.append(Paragraph("• <b>The Cool-down Phase:</b> During the final phase of the attack (intensity=0.3), detection confidence dropped significantly.", styles['BulletItem']))
    Story.append(Paragraph("• <b>Bursting Packets:</b> A 10% probability of bursting packets was introduced to briefly confuse the model.", styles['BulletItem']))
    Story.append(Paragraph("• <b>Reasoning:</b> Feature rolling windows need a 'warm-up' period to accumulate sufficient data. Rapidly oscillating behavior exploits this window before the rolling features stabilize.", styles['AlertText']))
    Story.append(Spacer(1, 0.2*inch))

    # Section 6 — Conclusion & Recommendations
    Story.append(Paragraph("Section 6 — Conclusion & Recommendations", styles['SectionHeader']))
    Story.append(Paragraph("Based on the investigation findings, the following actions are recommended to secure the IoT infrastructure:", styles['NormalText']))
    Story.append(Paragraph("1. <b>Deploy behavior-based AI detection:</b> Transition to ML-driven detection for IoT environments.", styles['BulletItem']))
    Story.append(Paragraph("2. <b>Implement time-series anomaly detection:</b> Focus on temporal metrics to identify low-profile malicious flows.", styles['BulletItem']))
    Story.append(Paragraph("3. <b>Use SHAP for model explainability:</b> In a production SOC, integrate SHAP to provide transparent insights into flagged traffic.", styles['BulletItem']))

    doc.build(Story)
    print(f"Report generated successfully at {output_path}")

if __name__ == "__main__":
    create_report()
