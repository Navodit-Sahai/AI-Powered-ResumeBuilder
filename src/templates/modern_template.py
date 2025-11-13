from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def generate_modern_docx(resume_data, output_dir, filename):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(0.75)
        s.left_margin = s.right_margin = Inches(1)

    info = resume_data.get('personal_info', {})
    name = doc.add_paragraph(info.get('name', '').upper())
    name.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = name.runs[0]
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 102, 204)
    doc.add_paragraph(f"{info.get('email', '')} • {info.get('phone', '')} • {info.get('location', '')}")

    if resume_data.get('skills'):
        doc.add_paragraph()
        h = doc.add_paragraph('CORE COMPETENCIES')
        hr = h.runs[0]
        hr.font.bold = True
        hr.font.size = Pt(14)
        hr.font.color.rgb = RGBColor(0, 102, 204)
        doc.add_paragraph(' • '.join(resume_data['skills']))

    if resume_data.get('summary'):
        doc.add_paragraph()
        h = doc.add_paragraph('PROFILE')
        hr = h.runs[0]
        hr.font.bold = True
        hr.font.size = Pt(14)
        hr.font.color.rgb = RGBColor(0, 102, 204)
        doc.add_paragraph(resume_data['summary'])

    path = os.path.join(output_dir, filename)
    doc.save(path)
    return path
