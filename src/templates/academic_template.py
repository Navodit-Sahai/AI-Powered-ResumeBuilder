from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def generate_academic_docx(resume_data, output_dir, filename):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)

    info = resume_data.get('personal_info', {})
    name = doc.add_paragraph(info.get('name', ''))
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.runs[0].font.size = Pt(18)
    name.runs[0].font.bold = True
    doc.add_paragraph(f"{info.get('email', '')} | {info.get('phone', '')}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    if resume_data.get('education'):
        doc.add_paragraph()
        h = doc.add_paragraph('EDUCATION')
        hr = h.runs[0]
        hr.font.bold = True
        hr.font.size = Pt(13)
        hr.underline = True
        for edu in resume_data['education']:
            p = doc.add_paragraph()
            p.add_run(edu.get('degree', '')).bold = True
            p.add_run(f"\n{edu.get('institution', '')}, {edu.get('year', '')}")
            if edu.get('gpa'):
                p.add_run(f"\nGPA: {edu['gpa']}")

    path = os.path.join(output_dir, filename)
    doc.save(path)
    return path
