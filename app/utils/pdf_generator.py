from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from app.models.invoice_model import Invoice

class PDFGenerator:
    """Generate professional PDF invoices using ReportLab."""
    
    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> BytesIO:
        """
        Generate a professional PDF invoice.
        
        Args:
            invoice: Invoice object with customer and project data
            
        Returns:
            BytesIO object containing the PDF
        """
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Header
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=1  # center
        )
        story.append(Paragraph("STONE BAR STUDIO", header_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            alignment=1
        )
        story.append(Paragraph("Custom Outdoor Stone Bars | San Antonio, TX", subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Invoice Title and Number
        invoice_title = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333')
        )
        story.append(Paragraph(f"INVOICE #{invoice.invoice_id}", invoice_title))
        story.append(Spacer(1, 0.15*inch))
        
        # Customer and Invoice Info Table
        info_data = [
            ["BILL TO", "INVOICE DATE"],
            [invoice.customer_name, invoice.date],
            [invoice.customer_address or "", ""],
            [invoice.customer_phone, ""],
            [invoice.customer_email, ""]
        ]
        
        info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Project Information
        project_title = ParagraphStyle(
            'ProjectTitle',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6
        )
        story.append(Paragraph("PROJECT DETAILS", project_title))
        
        project_info = [
            ["Project Name:", invoice.project_name],
            ["Bar Dimensions:", invoice.bom_data.get('top_dimensions', 'N/A')],
            ["Materials Required:", "See BOM below"]
        ]
        
        project_table = Table(project_info, colWidths=[2*inch, 5*inch])
        project_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(project_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Bill of Materials (if available)
        if invoice.bom_data:
            story.append(Paragraph("BILL OF MATERIALS", project_title))
            bom_items = [
                ["Item", "Quantity"]
            ]
            
            bom_mapping = {
                'lumber_ft': 'Lumber (2x4)',
                'plywood_sq_ft': 'Plywood (3/4" PT)',
                'lath_sq_ft': 'Metal Lath',
                'mortar_bags': 'Mortar Bags',
                'veneer_sq_ft': 'Stone Veneer',
                'top_sq_ft': 'Stone Countertop'
            }
            
            for key, label in bom_mapping.items():
                if key in invoice.bom_data:
                    value = invoice.bom_data[key]
                    unit = 'bags' if key == 'mortar_bags' else 'sq ft' if 'sq_ft' in key else 'ft'
                    bom_items.append([label, f"{value} {unit}"])
            
            bom_table = Table(bom_items, colWidths=[4*inch, 3*inch])
            bom_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            story.append(bom_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Pricing Section
        story.append(Paragraph("PRICING", project_title))
        pricing_data = [
            ["Description", "Amount"],
            ["Material Cost", f"${invoice.material_cost:,.2f}"],
            ["Labor Cost", f"${invoice.labor_cost:,.2f}"],
            ["TOTAL", f"${invoice.get_total_price():,.2f}"],
            ["", ""],
            ["Deposit (50%)", f"${invoice.get_deposit():,.2f}"],
            ["Balance Due", f"${invoice.get_balance_due():,.2f}"]
        ]
        
        pricing_table = Table(pricing_data, colWidths=[4*inch, 3*inch])
        pricing_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, 1), (-1, 2), 'Helvetica', 9),
            ('FONT', (0, 3), (-1, 3), 'Helvetica-Bold', 11),
            ('FONT', (0, 5), (-1, 6), 'Helvetica', 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#d9d9d9')),
            ('BACKGROUND', (0, 4), (-1, 4), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, 2), [colors.white, colors.HexColor('#f9f9f9')]),
            ('ROWBACKGROUNDS', (0, 5), (-1, 6), [colors.HexColor('#f0f0f0'), colors.white])
        ]))
        story.append(pricing_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=1
        )
        story.append(Paragraph("Thank you for choosing Stone Bar Studio!", footer_style))
        story.append(Paragraph("For questions, please contact us at Stone Bar Studio, San Antonio, TX", footer_style))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer