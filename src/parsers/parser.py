from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from typing import Dict, Any
import json

class ResumeParser:
    """Parses resume from PDF, DOCX, or manual input"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        loader = PyPDFLoader(file_path)
        documents = loader.load() 
        text = "\n".join([doc.page_content for doc in documents])
        return text
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        text = "\n".join([doc.page_content for doc in documents])
        return text
    
    @staticmethod
    def parse_manual_input(data: Dict[str, Any]) -> str:
        """Convert manual input dictionary to structured text"""
        sections = []
        
        # Personal Information
        if 'personal_info' in data:
            info = data['personal_info']
            sections.append(f"PERSONAL INFORMATION\n{info.get('name', '')}\n{info.get('email', '')}\n{info.get('phone', '')}\n{info.get('location', '')}")
        
        # Education
        if 'education' in data:
            sections.append("\nEDUCATION")
            for edu in data['education']:
                sections.append(f"{edu.get('degree', '')} - {edu.get('institution', '')} ({edu.get('year', '')})")
        
        # Skills
        if 'skills' in data:
            sections.append(f"\nSKILLS\n{', '.join(data['skills'])}")
        
        # Experience
        if 'experience' in data:
            sections.append("\nWORK EXPERIENCE")
            for exp in data['experience']:
                sections.append(f"{exp.get('title', '')} at {exp.get('company', '')} ({exp.get('duration', '')})")
                sections.append(f"{exp.get('description', '')}")
        
        # Projects
        if 'projects' in data:
            sections.append("\nPROJECTS")
            for proj in data['projects']:
                sections.append(f"{proj.get('name', '')}: {proj.get('description', '')}")
        
        return "\n".join(sections)

