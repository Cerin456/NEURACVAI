import openai
import os
import json
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

class AISuggestionsEngine:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            self.client = openai.OpenAI(api_key=api_key)
            self.use_ai = True
        else:
            self.use_ai = False
    
    def analyze_resume(self, resume_data: Dict) -> Dict:
        if self.use_ai:
            return self._get_ai_analysis(resume_data)
        else:
            return self._get_mock_analysis(resume_data)
    
    def _get_ai_analysis(self, resume_data: Dict) -> Dict:
        try:
            prompt = self._create_analysis_prompt(resume_data)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume coach and ATS specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            
            return self._parse_ai_response(response.choices[0].message.content)
        except Exception as e:
            return self._get_mock_analysis(resume_data)
    
    def _get_mock_analysis(self, resume_data: Dict) -> Dict:
        """Provide mock analysis when AI is not available"""
        return {
            'ats_score': 75,
            'suggestions': {
                'overall_feedback': [
                    "Add more quantifiable achievements to your experience section",
                    "Include specific numbers and metrics to show impact",
                    "Use strong action verbs like 'managed', 'developed', 'implemented'",
                    "Tailor your skills to match your target job descriptions",
                    "Consider adding a projects section to showcase practical experience"
                ],
                'section_feedback': {
                    'personal_info': ["Ensure your summary is compelling and keyword-rich"],
                    'experience': ["Focus on accomplishments rather than responsibilities"],
                    'skills': ["Categorize skills (technical vs soft skills)"]
                },
                'missing_keywords': ['leadership', 'management', 'optimization', 'strategy', 'analysis']
            },
            'improved_content': resume_data
        }
    
    def _create_analysis_prompt(self, resume_data: Dict) -> str:
        return f"""
        Analyze this resume data and provide constructive feedback:
        
        {json.dumps(resume_data, indent=2)}
        
        Provide feedback in this JSON format:
        {{
            "ats_score": 0-100,
            "suggestions": {{
                "overall_feedback": ["list of suggestions"],
                "section_feedback": {{
                    "personal_info": ["suggestions"],
                    "experience": ["suggestions"],
                    "skills": ["suggestions"]
                }},
                "missing_keywords": ["list of keywords"]
            }},
            "improved_content": {resume_data}
        }}
        """
    
    def _parse_ai_response(self, response: str) -> Dict:
        try:
            return json.loads(response)
        except:
            return self._get_mock_analysis({})

def get_ai_suggestions(resume_data: Dict) -> Dict:
    engine = AISuggestionsEngine()
    return engine.analyze_resume(resume_data)