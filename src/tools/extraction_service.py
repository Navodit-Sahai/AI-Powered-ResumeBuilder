from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic_objects import EnhancedResume
from pydantic import ValidationError
import json
import re


class ResumeExtractor:
    def __init__(self, resume_text: str):
        load_dotenv()
        self.resume_text = resume_text
        print(resume_text)
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        self.prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
You are an intelligent resume parsing assistant.

Extract structured data from the following resume text and output it as valid JSON strictly matching this format:

{{
  "personal_info": {{
    "name": "",
    "email": "",
    "phone": "",
    "location": ""
  }},
  "summary": "",
  "education": [
    {{"degree": "", "institution": "", "year": ""}}
  ],
  "skills": [],
  "experience": [
    {{"title": "", "company": "", "duration": "", "description": ""}}
  ],
  "projects": [
    {{"name": "", "description": ""}}
  ]
}}

Resume:
{resume_text}

IMPORTANT: Return ONLY valid JSON. No markdown, no code blocks, no commentary.
"""
        )

    def extraction(self):
        try:
            formatted_prompt = self.prompt.format(resume_text=self.resume_text)
            response = self.llm.invoke(formatted_prompt)
            result = response.content.strip()
            result = re.sub(r'```json\s*', '', result)
            result = re.sub(r'```\s*', '', result)
            result = result.strip()
            parsed_json = json.loads(result)
            validated = EnhancedResume(**parsed_json)
            return validated

        except json.JSONDecodeError as e:
            raise ValueError(f" Model did not return valid JSON. Error: {e}\nResponse: {result[:200]}")
        except ValidationError as e:
            raise ValueError(f" Parsed data did not match EnhancedResume schema:\n{e}")
        except Exception as e:
            raise RuntimeError(f" Error during extraction: {e}")