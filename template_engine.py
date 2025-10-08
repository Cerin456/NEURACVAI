import streamlit as st
from jinja2 import Template
import os

def render_template(template_name: str, resume_data: dict, improved: bool = False) -> str:
    """Render resume template with data"""
    
    # If improved version is requested and available, use it
    if improved and 'ai_analysis' in st.session_state:
        improved_content = st.session_state.ai_analysis.get('improved_content', {})
        if improved_content:
            resume_data = improved_content
    
    template_file = f"templates/{template_name}.html"
    
    # If template file doesn't exist, use basic template
    if not os.path.exists(template_file):
        return render_basic_template(resume_data, improved)
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        return template.render(
            data=resume_data,
            improved=improved,
            **resume_data
        )
    except Exception as e:
        st.error(f"Error loading template: {str(e)}")
        return render_basic_template(resume_data, improved)

def render_basic_template(resume_data: dict, improved: bool = False) -> str:
    """Basic HTML template as fallback"""
    personal_info = resume_data.get('personal_info', {})
    experience = resume_data.get('experience', [])
    education = resume_data.get('education', [])
    technical_skills = resume_data.get('technical_skills', [])
    soft_skills = resume_data.get('soft_skills', [])
    projects = resume_data.get('projects', [])
    certifications = resume_data.get('certifications', [])
    languages = resume_data.get('languages', [])
    
    improved_badge = "🎯 AI-IMPROVED VERSION" if improved else ""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{personal_info.get('name', 'Resume')}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .resume-container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #2E86AB;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .name {{
                font-size: 32px;
                font-weight: bold;
                color: #2E86AB;
                margin: 0;
            }}
            .improved-badge {{
                background: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                margin-left: 10px;
            }}
            .contact-info {{
                color: #666;
                margin-top: 10px;
                font-size: 14px;
            }}
            .section {{
                margin: 25px 0;
            }}
            .section-title {{
                font-size: 20px;
                font-weight: bold;
                color: #2E86AB;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 8px;
                margin-bottom: 15px;
            }}
            .experience-item, .education-item, .project-item {{
                margin: 15px 0;
                padding-left: 10px;
                border-left: 3px solid #2E86AB;
            }}
            .job-title {{
                font-weight: bold;
                font-size: 16px;
                color: #333;
            }}
            .company {{
                color: #666;
                font-style: italic;
            }}
            .date {{
                color: #888;
                font-size: 14px;
            }}
            .skills-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 10px;
            }}
            .skill-tag {{
                background: #2E86AB;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 14px;
            }}
            .soft-skill-tag {{
                background: #A23B72;
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 14px;
            }}
            .project-link {{
                color: #2E86AB;
                text-decoration: none;
            }}
            .project-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="resume-container">
            <div class="header">
                <div class="name">
                    {personal_info.get('name', 'Your Name')}
                    {f'<span class="improved-badge">{improved_badge}</span>' if improved_badge else ''}
                </div>
                <div class="contact-info">
                    {personal_info.get('email', '')} | 
                    {personal_info.get('phone', '')} | 
                    {personal_info.get('location', '')}
                    {('<br>LinkedIn: ' + personal_info.get('linkedin', '')) if personal_info.get('linkedin') else ''}
                    {('<br>GitHub: ' + personal_info.get('github', '')) if personal_info.get('github') else ''}
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">Professional Summary</div>
                <p>{personal_info.get('summary', 'Professional summary not provided.')}</p>
            </div>
            
            {f'''
            <div class="section">
                <div class="section-title">Work Experience</div>
                {"".join([f'''
                <div class="experience-item">
                    <div class="job-title">{exp.get('title', 'Position')}</div>
                    <div class="company">{exp.get('company', 'Company')}</div>
                    <div class="date">{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}</div>
                    <p>{exp.get('description', 'Description not provided.')}</p>
                </div>
                ''' for exp in experience])}
            </div>
            ''' if experience else ''}
            
            {f'''
            <div class="section">
                <div class="section-title">Education</div>
                {"".join([f'''
                <div class="education-item">
                    <div class="job-title">{edu.get('degree', 'Degree')}</div>
                    <div class="company">{edu.get('institution', 'Institution')}</div>
                    <div class="date">{edu.get('year', 'Year')}{' | GPA: ' + edu.get('gpa', '') if edu.get('gpa') else ''}</div>
                    {('<p><em>Relevant coursework: ' + edu.get('courses', '') + '</em></p>') if edu.get('courses') else ''}
                </div>
                ''' for edu in education])}
            </div>
            ''' if education else ''}
            
            {(f'''
            <div class="section">
                <div class="section-title">Technical Skills</div>
                <div class="skills-container">
                    {"".join([f'<div class="skill-tag">{skill}</div>' for skill in technical_skills])}
                </div>
            </div>
            ''') if technical_skills else ''}
            
            {(f'''
            <div class="section">
                <div class="section-title">Soft Skills</div>
                <div class="skills-container">
                    {"".join([f'<div class="soft-skill-tag">{skill}</div>' for skill in soft_skills])}
                </div>
            </div>
            ''') if soft_skills else ''}
            
            {f'''
            <div class="section">
                <div class="section-title">Projects</div>
                {"".join([f'''
                <div class="project-item">
                    <div class="job-title">{project.get('name', 'Project')}</div>
                    {('<div><a href="{project.get("url", "")}" class="project-link">View Project</a></div>') if project.get('url') else ''}
                    <p>{project.get('description', 'Description not provided.')}</p>
                </div>
                ''' for project in projects])}
            </div>
            ''' if projects else ''}
            
            {(f'''
            <div class="section">
                <div class="section-title">Certifications & Awards</div>
                <div class="skills-container">
                    {"".join([f'<div class="skill-tag">{cert}</div>' for cert in certifications])}
                </div>
            </div>
            ''') if certifications else ''}
            
            {(f'''
            <div class="section">
                <div class="section-title">Languages</div>
                <div class="skills-container">
                    {"".join([f'<div class="soft-skill-tag">{lang}</div>' for lang in languages])}
                </div>
            </div>
            ''') if languages else ''}
        </div>
    </body>
    </html>
    """
    
    return html

def get_all_templates() -> dict:
    """Get all available templates"""
    return {
        'professional': {
            'name': 'Professional',
            'description': 'Clean and professional design for corporate roles',
            'color': '#2E86AB',
            'preview': '👔'
        },
        'modern': {
            'name': 'Modern',
            'description': 'Contemporary design with creative elements',
            'color': '#A23B72',
            'preview': '🎨'
        },
        'creative': {
            'name': 'Creative',
            'description': 'Innovative layout perfect for design and tech roles',
            'color': '#F18F01',
            'preview': '💡'
        }
    }

def create_template_files():
    """Create basic template files if they don't exist"""
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # Create professional template
    professional_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'Arial', sans-serif; margin: 40px; line-height: 1.6; }
            .header { border-bottom: 2px solid #2c3e50; padding-bottom: 20px; }
            .name { font-size: 28px; color: #2c3e50; font-weight: bold; }
            .contact { color: #7f8c8d; margin-top: 5px; }
            .section { margin: 25px 0; }
            .section-title { font-size: 18px; color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }
            .job { margin: 15px 0; }
            .job-title { font-weight: bold; }
            .company { color: #34495e; font-style: italic; }
            .skills { display: flex; flex-wrap: wrap; gap: 8px; }
            .skill { background: #3498db; color: white; padding: 4px 8px; border-radius: 3px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="name">{{ data.personal_info.name }}</div>
            <div class="contact">
                {{ data.personal_info.email }} | {{ data.personal_info.phone }} | {{ data.personal_info.location }}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Professional Summary</div>
            <p>{{ data.personal_info.summary }}</p>
        </div>
        
        <div class="section">
            <div class="section-title">Experience</div>
            {% for exp in data.experience %}
            <div class="job">
                <div class="job-title">{{ exp.title }}</div>
                <div class="company">{{ exp.company }} | {{ exp.start_date }} - {{ exp.end_date or 'Present' }}</div>
                <p>{{ exp.description }}</p>
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <div class="section-title">Education</div>
            {% for edu in data.education %}
            <div class="job">
                <div class="job-title">{{ edu.degree }}</div>
                <div class="company">{{ edu.institution }} | {{ edu.year }}</div>
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <div class="section-title">Skills</div>
            <div class="skills">
                {% for skill in data.technical_skills %}
                <span class="skill">{{ skill }}</span>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, "professional.html"), "w", encoding="utf-8") as f:
        f.write(professional_html)
    
    return True