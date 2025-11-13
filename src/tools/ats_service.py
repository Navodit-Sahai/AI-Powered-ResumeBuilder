import requests
from typing import Dict, Any, List
import re

class ATSScorer:
    """Calculate ATS score and provide recommendations"""
    
    @staticmethod
    def calculate_score(resume_text: str, job_description: str = "") -> Dict[str, Any]:
        """Calculate ATS score based on various criteria"""
        score = 0
        max_score = 100
        feedback = []
        
        # Check for keywords (20 points)
        keyword_score = ATSScorer._check_keywords(resume_text, job_description)
        score += keyword_score
        if keyword_score < 15:
            feedback.append("Add more relevant keywords from the job description")
        
        # Check formatting (20 points)
        format_score = ATSScorer._check_formatting(resume_text)
        score += format_score
        if format_score < 15:
            feedback.append("Improve resume structure and formatting")
        
        # Check for contact information (10 points)
        contact_score = ATSScorer._check_contact_info(resume_text)
        score += contact_score
        if contact_score < 8:
            feedback.append("Ensure all contact information is present")
        
        # Check for quantifiable achievements (20 points)
        achievement_score = ATSScorer._check_achievements(resume_text)
        score += achievement_score
        if achievement_score < 15:
            feedback.append("Include more quantifiable achievements")
        
        # Check length (10 points)
        length_score = ATSScorer._check_length(resume_text)
        score += length_score
        
        # Check for action verbs (20 points)
        action_score = ATSScorer._check_action_verbs(resume_text)
        score += action_score
        if action_score < 15:
            feedback.append("Use more strong action verbs")
        
        return {
            "score": min(score, max_score),
            "max_score": max_score,
            "feedback": feedback,
            "breakdown": {
                "keywords": keyword_score,
                "formatting": format_score,
                "contact_info": contact_score,
                "achievements": achievement_score,
                "length": length_score,
                "action_verbs": action_score
            }
        }
    
    def _check_keywords(text: str, job_desc: str) -> int:
        """Check for relevant keywords"""
        common_keywords = ['python', 'java', 'javascript', 'react', 'sql', 'aws', 
                          'docker', 'kubernetes', 'agile', 'team', 'leadership']
        text_lower = text.lower()
        found = sum(1 for kw in common_keywords if kw in text_lower)
        return min(int((found / len(common_keywords)) * 20), 20)
    
    def _check_formatting(text: str) -> int:
        """Check resume structure"""
        required_sections = ['education', 'experience', 'skills']
        text_lower = text.lower()
        found = sum(1 for section in required_sections if section in text_lower)
        return int((found / len(required_sections)) * 20)

    def _check_contact_info(text: str) -> int:
        """Check for contact information"""
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text))
        score = 0
        if has_email: score += 5
        if has_phone: score += 5
        return score
    
    def _check_achievements(text: str) -> int:
        """Check for quantifiable achievements"""
        numbers = re.findall(r'\b\d+%|\b\d+\+|\$\d+|\b\d+ (?:years|months)', text)
        return min(len(numbers) * 4, 20)

    def _check_length(text: str) -> int:
        """Check resume length"""
        word_count = len(text.split())
        if 400 <= word_count <= 800:
            return 10
        elif 300 <= word_count <= 1000:
            return 7
        return 5
    
    def _check_action_verbs(text: str) -> int:
        """Check for strong action verbs"""
        action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 
                       'designed', 'achieved', 'improved', 'increased', 'reduced']
        text_lower = text.lower()
        found = sum(1 for verb in action_verbs if verb in text_lower)
        return min(int((found / len(action_verbs)) * 20), 20)