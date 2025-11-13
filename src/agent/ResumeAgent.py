from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, List

from src.parsers.parser import ResumeParser
from src.tools.ats_service import ATSScorer
from src.tools.enhance_service import Enhancer
from src.tools.render_service import ResumeGenerator


class ResumeAgent:
    """Agent orchestrating resume parsing, enhancement, and generation using Groq LLM"""

    def __init__(self):
        self.parser = ResumeParser()
        self.ats_scorer = ATSScorer()
        self.enhancer = Enhancer()
        self.generator = ResumeGenerator()

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )

        self.prompt = ChatPromptTemplate.from_template("""
        You are a professional Resume Assistant using Groq LLM.
        You help users:
        1. Parse resumes (PDF/DOCX/manual)
        2. Score resumes for ATS
        3. Enhance content professionally
        4. Generate resumes in DOCX and PDF
        5. Provide helpful feedback and improvements.

        When asked a question, decide which step to execute and respond with helpful guidance.
        User input: {input}
        """)

    def process_resume(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Full resume processing pipeline"""
        results = {}
        if 'file_path' in input_data:
            file_path = input_data['file_path']
            if file_path.endswith('.pdf'):
                resume_text = self.parser.parse_pdf(file_path)
            elif file_path.endswith('.docx'):
                resume_text = self.parser.parse_docx(file_path)
            else:
                raise ValueError("Unsupported file type")
        else:
            resume_text = self.parser.parse_manual_input(input_data)
        results['original_text'] = resume_text

        results['initial_score'] = self.ats_scorer.calculate_score(resume_text)

        enhanced_text = self.enhancer.enhance_with_groq(resume_text)
        results['enhanced_text'] = enhanced_text

        results['final_score'] = self.ats_scorer.calculate_score(enhanced_text)

        docx_path = self.generator.generate_docx(input_data)
        pdf_path = self.generator.generate_pdf(input_data)
        results['docx_path'] = docx_path
        results['pdf_path'] = pdf_path

        return results

    def chat(self, message: str, chat_history: List = None) -> str:
        """Chat-like interaction """
        if chat_history is None:
            chat_history = []
        formatted_prompt = self.prompt.format(input=message)
        response = self.llm.invoke(formatted_prompt)
        return response.content.strip()
