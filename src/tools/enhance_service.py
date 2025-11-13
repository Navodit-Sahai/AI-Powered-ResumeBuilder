from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic_objects import EnhancedResume
from dotenv import load_dotenv
import json

class Enhancer:
    def __init__(self, structured_input: dict):
        load_dotenv()
        self.structured_input = structured_input
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        self.prompt = PromptTemplate(
            input_variables=["structured_input"],
            template="""
You are a professional resume optimization assistant.

Given the following structured resume data in JSON format, 
improve it by rewriting each section with professional phrasing, 
action-oriented tone, and keyword optimization for ATS systems. 

Keep the JSON structure identical. Do not add commentary or markdown.
Return only the improved JSON.

Structured Resume:
{structured_input}
"""
        )

    def enhance(self):
        try:
            input_json_str = json.dumps(self.structured_input, indent=2)
            formatted_prompt = self.prompt.format(structured_input=input_json_str)
            response = self.llm.invoke(formatted_prompt)
            result = response.content.strip()
            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            enhanced_data = json.loads(result)
            validated = EnhancedResume(**enhanced_data)
            return validated
        except Exception as e:
            raise RuntimeError(f"Error during enhancement: {e}")
