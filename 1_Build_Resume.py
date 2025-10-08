import streamlit as st
from utils.ai_suggestions import get_ai_suggestions
from utils.resume_parser import parse_resume

def show_build_resume():
    st.title("📄 Build Your Resume")
    st.markdown("---")
    
    # Initialize session state
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'personal_info': {},
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'certifications': [],
            'languages': []
        }
    
    # Initialize experience and education lists
    if 'experience' not in st.session_state:
        st.session_state.experience = st.session_state.resume_data.get('experience', [{}])
    
    if 'education' not in st.session_state:
        st.session_state.education = st.session_state.resume_data.get('education', [{}])
    
    if 'projects' not in st.session_state:
        st.session_state.projects = st.session_state.resume_data.get('projects', [{}])
    
    # File upload section (OUTSIDE the form)
    st.header("📤 Upload Existing Resume (Optional)")
    uploaded_file = st.file_uploader(
        "Upload your existing resume to auto-fill the form",
        type=['pdf', 'docx'],
        help="We'll parse your resume and pre-fill the information below"
    )
    
    if uploaded_file is not None:
        with st.spinner("🔍 Parsing your resume..."):
            try:
                parsed_data = parse_resume(uploaded_file)
                if parsed_data:
                    st.session_state.resume_data.update(parsed_data)
                    st.session_state.experience = st.session_state.resume_data.get('experience', [{}])
                    st.session_state.education = st.session_state.resume_data.get('education', [{}])
                    st.session_state.projects = st.session_state.resume_data.get('projects', [{}])
                    st.success("✅ Resume parsed successfully! Form pre-filled below.")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error parsing file: {str(e)}")
    
    # Experience management buttons (OUTSIDE the form)
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("➕ Add Another Experience", use_container_width=True):
            st.session_state.experience.append({})
            st.rerun()
    with col_exp2:
        if len(st.session_state.experience) > 1:
            if st.button("🗑️ Remove Last Experience", use_container_width=True):
                st.session_state.experience.pop()
                st.rerun()
    
    # Education management buttons (OUTSIDE the form)
    col_edu1, col_edu2 = st.columns(2)
    with col_edu1:
        if st.button("➕ Add Another Education", use_container_width=True):
            st.session_state.education.append({})
            st.rerun()
    with col_edu2:
        if len(st.session_state.education) > 1:
            if st.button("🗑️ Remove Last Education", use_container_width=True):
                st.session_state.education.pop()
                st.rerun()
    
    # Projects management buttons (OUTSIDE the form)
    col_proj1, col_proj2 = st.columns(2)
    with col_proj1:
        if st.button("➕ Add Another Project", use_container_width=True):
            st.session_state.projects.append({})
            st.rerun()
    
    # Main form
    with st.form("resume_builder", clear_on_submit=False):
        st.markdown("### 👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name*", 
                value=st.session_state.resume_data.get('personal_info', {}).get('name', ''),
                placeholder="John Doe"
            )
            email = st.text_input(
                "Email Address*", 
                value=st.session_state.resume_data.get('personal_info', {}).get('email', ''),
                placeholder="john.doe@email.com"
            )
            phone = st.text_input(
                "Phone Number*", 
                value=st.session_state.resume_data.get('personal_info', {}).get('phone', ''),
                placeholder="+1 (555) 123-4567"
            )
            
        with col2:
            linkedin = st.text_input(
                "LinkedIn Profile URL", 
                value=st.session_state.resume_data.get('personal_info', {}).get('linkedin', ''),
                placeholder="https://linkedin.com/in/johndoe"
            )
            github = st.text_input(
                "GitHub/Portfolio URL", 
                value=st.session_state.resume_data.get('personal_info', {}).get('github', ''),
                placeholder="https://github.com/johndoe"
            )
            location = st.text_input(
                "Location*", 
                value=st.session_state.resume_data.get('personal_info', {}).get('location', ''),
                placeholder="City, State, Country"
            )
        
        # Professional Summary
        st.markdown("### 📝 Professional Summary")
        summary = st.text_area(
            "Write a compelling professional summary (2-3 sentences)*",
            height=120,
            value=st.session_state.resume_data.get('personal_info', {}).get('summary', ''),
            placeholder="Experienced software engineer with 5+ years in full-stack development. Specialized in Python, React, and cloud technologies. Passionate about building scalable applications and leading cross-functional teams.",
            help="Highlight your key achievements, skills, and career objectives"
        )
        
        # Work Experience Section
        st.markdown("### 💼 Work Experience")
        
        for i, exp in enumerate(st.session_state.experience):
            with st.expander(f"🎯 Experience {i+1}", expanded=i==0):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    job_title = st.text_input(
                        f"Job Title*", 
                        key=f"exp_title_{i}", 
                        value=exp.get('title', ''),
                        placeholder="Senior Software Engineer"
                    )
                
                with col2:
                    company = st.text_input(
                        f"Company*", 
                        key=f"exp_company_{i}", 
                        value=exp.get('company', ''),
                        placeholder="Tech Company Inc."
                    )
                
                with col3:
                    col3a, col3b = st.columns(2)
                    with col3a:
                        start_date = st.text_input(
                            f"Start Date*", 
                            key=f"exp_start_{i}", 
                            value=exp.get('start_date', ''),
                            placeholder="Jan 2020"
                        )
                    with col3b:
                        end_date = st.text_input(
                            f"End Date", 
                            key=f"exp_end_{i}", 
                            value=exp.get('end_date', ''),
                            placeholder="Present"
                        )
                
                description = st.text_area(
                    f"Description & Achievements*", 
                    key=f"exp_desc_{i}", 
                    value=exp.get('description', ''),
                    height=100,
                    placeholder="• Led a team of 5 developers to deliver a new SaaS product\n• Improved application performance by 40% through optimization\n• Implemented CI/CD pipeline reducing deployment time by 60%\n• Managed project budget of $500K and delivered ahead of schedule",
                    help="Use bullet points. Focus on achievements and quantify results with numbers."
                )
        
        # Education Section
        st.markdown("### 🎓 Education")
        
        for i, edu in enumerate(st.session_state.education):
            with st.expander(f"📚 Education {i+1}", expanded=i==0):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    degree = st.text_input(
                        f"Degree/Certificate*", 
                        key=f"edu_degree_{i}", 
                        value=edu.get('degree', ''),
                        placeholder="Bachelor of Science in Computer Science"
                    )
                
                with col2:
                    institution = st.text_input(
                        f"Institution*", 
                        key=f"edu_institution_{i}", 
                        value=edu.get('institution', ''),
                        placeholder="University of Technology"
                    )
                
                with col3:
                    col3a, col3b = st.columns(2)
                    with col3a:
                        grad_year = st.text_input(
                            f"Graduation Year*", 
                            key=f"edu_year_{i}", 
                            value=edu.get('year', ''),
                            placeholder="2020"
                        )
                    with col3b:
                        gpa = st.text_input(
                            f"GPA", 
                            key=f"edu_gpa_{i}", 
                            value=edu.get('gpa', ''),
                            placeholder="3.8/4.0"
                        )
                
                courses = st.text_input(
                    f"Relevant Coursework/Achievements", 
                    key=f"edu_courses_{i}", 
                    value=edu.get('courses', ''),
                    placeholder="Data Structures, Algorithms, Machine Learning, Dean's List"
                )
        
        # Skills Section
        st.markdown("### 🛠️ Skills")
        
        col_skills1, col_skills2 = st.columns(2)
        
        with col_skills1:
            technical_skills = st.text_area(
                "Technical Skills*",
                height=100,
                value=", ".join(st.session_state.resume_data.get('technical_skills', [])),
                placeholder="Python, JavaScript, React, Node.js, SQL, AWS, Docker, Git, Machine Learning, Data Analysis",
                help="List your technical skills, programming languages, tools, and technologies"
            )
        
        with col_skills2:
            soft_skills = st.text_area(
                "Soft Skills & Professional Skills",
                height=100,
                value=", ".join(st.session_state.resume_data.get('soft_skills', [])),
                placeholder="Project Management, Leadership, Communication, Problem Solving, Team Collaboration, Agile Methodology",
                help="List your soft skills and professional competencies"
            )
        
        # Projects Section
        st.markdown("### 🚀 Projects")
        
        for i, project in enumerate(st.session_state.projects):
            with st.expander(f"💻 Project {i+1}", expanded=i==0):
                project_name = st.text_input(
                    f"Project Name*", 
                    key=f"proj_name_{i}", 
                    value=project.get('name', ''),
                    placeholder="E-commerce Platform"
                )
                
                project_url = st.text_input(
                    f"Project URL/GitHub", 
                    key=f"proj_url_{i}", 
                    value=project.get('url', ''),
                    placeholder="https://github.com/username/project"
                )
                
                project_desc = st.text_area(
                    f"Project Description*", 
                    key=f"proj_desc_{i}", 
                    value=project.get('description', ''),
                    height=80,
                    placeholder="Developed a full-stack e-commerce platform with React and Node.js. Implemented user authentication, payment processing, and inventory management.",
                    help="Describe the project, your role, technologies used, and outcomes"
                )
        
        # Certifications & Languages
        st.markdown("### 🏆 Certifications & Languages")
        
        col_cert1, col_cert2 = st.columns(2)
        
        with col_cert1:
            certifications = st.text_area(
                "Certifications & Awards",
                height=80,
                value=", ".join(st.session_state.resume_data.get('certifications', [])),
                placeholder="AWS Certified Solutions Architect, Google Professional Data Engineer, Scrum Master Certification",
                help="List relevant certifications, awards, and honors"
            )
        
        with col_cert2:
            languages = st.text_area(
                "Languages",
                height=80,
                value=", ".join(st.session_state.resume_data.get('languages', [])),
                placeholder="English (Native), Spanish (Professional), French (Basic)",
                help="List languages you speak and proficiency levels"
            )
        
        # SUBMIT BUTTON - This is the correct way inside a form
        submitted = st.form_submit_button("🤖 Save Resume & Generate AI Analysis", type="primary", use_container_width=True)
        
        if submitted:
            # Validate required fields
            if not name or not email or not summary:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                # Collect all form data
                experience_data = []
                for i in range(len(st.session_state.experience)):
                    title = st.session_state.get(f'exp_title_{i}', '')
                    company = st.session_state.get(f'exp_company_{i}', '')
                    if title and company:
                        experience_data.append({
                            'title': title,
                            'company': company,
                            'start_date': st.session_state.get(f'exp_start_{i}', ''),
                            'end_date': st.session_state.get(f'exp_end_{i}', ''),
                            'description': st.session_state.get(f'exp_desc_{i}', '')
                        })
                
                education_data = []
                for i in range(len(st.session_state.education)):
                    degree = st.session_state.get(f'edu_degree_{i}', '')
                    institution = st.session_state.get(f'edu_institution_{i}', '')
                    if degree and institution:
                        education_data.append({
                            'degree': degree,
                            'institution': institution,
                            'year': st.session_state.get(f'edu_year_{i}', ''),
                            'gpa': st.session_state.get(f'edu_gpa_{i}', ''),
                            'courses': st.session_state.get(f'edu_courses_{i}', '')
                        })
                
                projects_data = []
                for i in range(len(st.session_state.projects)):
                    name = st.session_state.get(f'proj_name_{i}', '')
                    if name:
                        projects_data.append({
                            'name': name,
                            'url': st.session_state.get(f'proj_url_{i}', ''),
                            'description': st.session_state.get(f'proj_desc_{i}', '')
                        })
                
                # Save data to session state
                st.session_state.resume_data = {
                    'personal_info': {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'linkedin': linkedin,
                        'github': github,
                        'location': location,
                        'summary': summary
                    },
                    'experience': experience_data,
                    'education': education_data,
                    'technical_skills': [skill.strip() for skill in technical_skills.split(',') if skill.strip()],
                    'soft_skills': [skill.strip() for skill in soft_skills.split(',') if skill.strip()],
                    'projects': projects_data,
                    'certifications': [cert.strip() for cert in certifications.split(',') if cert.strip()],
                    'languages': [lang.strip() for lang in languages.split(',') if lang.strip()]
                }
                
                st.success("✅ Resume data saved successfully!")
                
                # Generate AI suggestions
                with st.spinner("🤖 Generating AI analysis and suggestions..."):
                    try:
                        st.session_state.ai_analysis = get_ai_suggestions(st.session_state.resume_data)
                        st.success("🎯 AI analysis complete! Check the 'Preview & AI' page.")
                    except Exception as e:
                        st.error(f"❌ AI analysis failed: {str(e)}")
                        # Provide fallback suggestions
                        st.session_state.ai_analysis = {
                            'ats_score': 70,
                            'suggestions': {
                                'overall_feedback': [
                                    "Add more quantifiable achievements to your experience section",
                                    "Include specific technical skills relevant to your target roles",
                                    "Use action verbs and focus on accomplishments rather than responsibilities"
                                ]
                            }
                        }
                        st.info("💡 Basic analysis provided. For full AI features, check your API configuration.")

if __name__ == "__main__":
    show_build_resume()