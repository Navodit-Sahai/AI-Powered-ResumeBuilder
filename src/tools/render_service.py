from typing import Dict, Any
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from src.templates.professional_template import generate_professional_docx
from src.templates.modern_template import generate_modern_docx
from src.templates.academic_template import generate_academic_docx


class ResumeGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_docx(self, resume_data: Dict[str, Any], template_style: str = "professional", filename: str = "resume.docx") -> str:
        if template_style == "modern":
            return generate_modern_docx(resume_data, self.output_dir, filename)
        elif template_style == "academic":
            return generate_academic_docx(resume_data, self.output_dir, filename)
        return generate_professional_docx(resume_data, self.output_dir, filename)

    def generate_pdf(self, resume_data: Dict[str, Any], template_style: str = "professional", filename: str = "resume.pdf") -> str:
        path = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_color = colors.HexColor('#0066CC') if template_style == "modern" else colors.black
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=title_color, alignment=1)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, textColor=title_color, spaceAfter=6, spaceBefore=12)

        info = resume_data.get('personal_info', {})
        story.append(Paragraph(info.get('name', ''), title_style))
        story.append(Paragraph(f"{info.get('email', '')} | {info.get('phone', '')} | {info.get('location', '')}", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

        if resume_data.get('summary'):
            story.append(Paragraph('PROFESSIONAL SUMMARY', heading_style))
            story.append(Paragraph(resume_data['summary'], styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

        section_order = {
            "professional": ['education', 'skills', 'experience', 'projects'],
            "modern": ['skills', 'experience', 'projects', 'education'],
            "academic": ['education', 'experience', 'projects', 'skills']
        }

        for section in section_order.get(template_style, section_order['professional']):
            if section == 'education' and resume_data.get('education'):
                story.append(Paragraph('EDUCATION', heading_style))
                for e in resume_data['education']:
                    story.append(Paragraph(f"<b>{e.get('degree', '')}</b><br/>{e.get('institution', '')} | {e.get('year', '')}", styles['Normal']))
            elif section == 'skills' and resume_data.get('skills'):
                story.append(Paragraph('SKILLS', heading_style))
                story.append(Paragraph(', '.join(resume_data['skills']), styles['Normal']))
            elif section == 'experience' and resume_data.get('experience'):
                story.append(Paragraph('WORK EXPERIENCE', heading_style))
                for e in resume_data['experience']:
                    story.append(Paragraph(f"<b>{e.get('title', '')}</b><br/>{e.get('company', '')} | {e.get('duration', '')}", styles['Normal']))
                    for r in e.get('responsibilities', []):
                        story.append(Paragraph(f"• {r}", styles['Normal']))
            elif section == 'projects' and resume_data.get('projects'):
                story.append(Paragraph('PROJECTS', heading_style))
                for p in resume_data['projects']:
                    story.append(Paragraph(f"<b>{p.get('name', '')}</b><br/>{p.get('description', '')}", styles['Normal']))

        doc.build(story)
        return path