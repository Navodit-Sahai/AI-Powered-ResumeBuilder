from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

class Enhancer:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        self.prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
You are a professional resume optimization assistant.

Enhance the following resume by:
1. Using strong action verbs and professional language
2. Making descriptions more impactful and quantifiable
3. Optimizing for ATS systems with relevant keywords
4. Maintaining clarity and readability

Return ONLY the enhanced resume text. No commentary or markdown.

Resume:
{resume_text}
"""
        )

    def enhance_with_groq(self, resume_text: str) -> str:
        formatted_prompt = self.prompt.format(resume_text=resume_text)
        response = self.llm.invoke(formatted_prompt)
        return response.content.strip()