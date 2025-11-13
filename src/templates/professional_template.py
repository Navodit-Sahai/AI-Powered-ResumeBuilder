from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def generate_professional_docx(resume_data, output_dir, filename):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    info = resume_data.get('personal_info', {})
    name = doc.add_paragraph(info.get('name', ''))
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.runs[0].font.size = Pt(20)
    name.runs[0].font.bold = True
    contact = doc.add_paragraph(f"{info.get('email', '')} | {info.get('phone', '')} | {info.get('location', '')}")
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if resume_data.get('summary'):
        doc.add_paragraph()
        doc.add_paragraph('PROFESSIONAL SUMMARY').runs[0].bold = True
        doc.add_paragraph(resume_data['summary'])

    if resume_data.get('education'):
        doc.add_paragraph()
        doc.add_paragraph('EDUCATION').runs[0].bold = True
        for edu in resume_data['education']:
            p = doc.add_paragraph()
            p.add_run(edu.get('degree', '')).bold = True
            p.add_run(f"\n{edu.get('institution', '')} | {edu.get('year', '')}")

    if resume_data.get('skills'):
        doc.add_paragraph()
        doc.add_paragraph('SKILLS').runs[0].bold = True
        doc.add_paragraph(', '.join(resume_data['skills']))

    if resume_data.get('experience'):
        doc.add_paragraph()
        doc.add_paragraph('WORK EXPERIENCE').runs[0].bold = True
        for exp in resume_data['experience']:
            p = doc.add_paragraph()
            p.add_run(exp.get('title', '')).bold = True
            p.add_run(f"\n{exp.get('company', '')} | {exp.get('duration', '')}")
            for r in exp.get('responsibilities', []):
                doc.add_paragraph(f"• {r}", style='List Bullet')

    if resume_data.get('projects'):
        doc.add_paragraph()
        doc.add_paragraph('PROJECTS').runs[0].bold = True
        for proj in resume_data['projects']:
            p = doc.add_paragraph()
            p.add_run(proj.get('name', '')).bold = True
            p.add_run(f"\n{proj.get('description', '')}")

    path = os.path.join(output_dir, filename)
    doc.save(path)
    return path
