from typing import List,Dict,Any
from pydantic import BaseModel,Field

class EnhancedResume(BaseModel):
    """Model for enhanced resume content"""
    personal_info: Dict[str, str] = Field(description="Personal information")
    summary: str = Field(description="Professional summary")
    education: List[Dict[str, str]] = Field(description="Education details")
    skills: List[str] = Field(description="Skills list")
    experience: List[Dict[str, Any]] = Field(description="Work experience")
    projects: List[Dict[str, str]] = Field(description="Projects")