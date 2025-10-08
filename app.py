import streamlit as st
from streamlit_option_menu import option_menu
from utils.ai_suggestions import get_ai_suggestions
from utils.template_engine import render_template, get_all_templates
from utils.resume_parser import parse_resume

# Page configuration
st.set_page_config(
    page_title="NEURACV - AI Resume Builder",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        border-left: 5px solid #667eea;
        padding-left: 15px;
        margin: 2rem 0 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="main-header">🧠 NEURACV</div>', unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Build Resume", "Templates", "Preview & AI"],
            icons=["house", "pencil", "palette", "robot"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#0E1117"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "color": "white",
                    "--hover-color": "#262730",
                },
                "nav-link-selected": {"background-color": "#4CAF50"},
            }
        )
    
    # Page routing - ALL IN ONE FILE
    if selected == "Home":
        show_homepage()
    elif selected == "Build Resume":
        show_build_resume()
    elif selected == "Templates":
        show_templates()
    elif selected == "Preview & AI":
        show_preview_ai()

def show_homepage():
    st.title("🚀 NEURACV - AI-Powered Resume Builder")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Create Professional Resumes with AI Assistance")
        st.markdown("""
        ### ✨ Features:
        - **📤 Document Upload** - Upload existing resumes (PDF/DOCX)
        - **🤖 AI-Powered Analysis** - Get intelligent feedback and suggestions
        - **🎯 ATS Optimization** - Optimized for Applicant Tracking Systems
        - **🎨 Multiple Templates** - Choose from professionally designed templates
        - **📊 Real-time Analysis** - See AI suggestions instantly
        - **📥 Easy Export** - Download in multiple formats
        
        ### 🎯 How it works:
        1. **Upload or Build** - Upload existing resume or build from scratch
        2. **AI Analysis** - Get instant AI feedback and improvements
        3. **Choose Template** - Select from beautiful templates
        4. **Preview & Download** - Finalize and export your resume
        """)
    
    with col2:
        # Feature highlights
        st.info("""
        **🎯 Pro Tips:**
        - Use action verbs in your bullet points
        - Quantify your achievements with numbers
        - Keep it concise (1-2 pages maximum)
        - Tailor for each job application
        - Include relevant keywords from job descriptions
        """)

def show_build_resume():
    st.title("📄 Build Your Resume")
    st.markdown("---")
    
    # Initialize session state
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'personal_info': {},
            'experience': [],
            'education': [],
            'technical_skills': [],
            'soft_skills': [],
            'projects': [],
            'certifications': [],
            'languages': []
        }
    
    # Initialize lists
    if 'experience' not in st.session_state:
        st.session_state.experience = st.session_state.resume_data.get('experience', [{}])
    
    if 'education' not in st.session_state:
        st.session_state.education = st.session_state.resume_data.get('education', [{}])
    
    if 'projects' not in st.session_state:
        st.session_state.projects = st.session_state.resume_data.get('projects', [{}])
    
    # File upload section
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
    
    # Experience management buttons
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
    
    # Education management buttons
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
    
    # Projects management buttons
    if st.button("➕ Add Project", use_container_width=True):
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
                    st.text_input(
                        f"Job Title*", 
                        key=f"exp_title_{i}", 
                        value=exp.get('title', ''),
                        placeholder="Senior Software Engineer"
                    )
                
                with col2:
                    st.text_input(
                        f"Company*", 
                        key=f"exp_company_{i}", 
                        value=exp.get('company', ''),
                        placeholder="Tech Company Inc."
                    )
                
                with col3:
                    col3a, col3b = st.columns(2)
                    with col3a:
                        st.text_input(
                            f"Start Date*", 
                            key=f"exp_start_{i}", 
                            value=exp.get('start_date', ''),
                            placeholder="Jan 2020"
                        )
                    with col3b:
                        st.text_input(
                            f"End Date", 
                            key=f"exp_end_{i}", 
                            value=exp.get('end_date', ''),
                            placeholder="Present"
                        )
                
                st.text_area(
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
                    st.text_input(
                        f"Degree/Certificate*", 
                        key=f"edu_degree_{i}", 
                        value=edu.get('degree', ''),
                        placeholder="Bachelor of Science in Computer Science"
                    )
                
                with col2:
                    st.text_input(
                        f"Institution*", 
                        key=f"edu_institution_{i}", 
                        value=edu.get('institution', ''),
                        placeholder="University of Technology"
                    )
                
                with col3:
                    col3a, col3b = st.columns(2)
                    with col3a:
                        st.text_input(
                            f"Graduation Year*", 
                            key=f"edu_year_{i}", 
                            value=edu.get('year', ''),
                            placeholder="2020"
                        )
                    with col3b:
                        st.text_input(
                            f"GPA", 
                            key=f"edu_gpa_{i}", 
                            value=edu.get('gpa', ''),
                            placeholder="3.8/4.0"
                        )
                
                st.text_input(
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
                st.text_input(
                    f"Project Name*", 
                    key=f"proj_name_{i}", 
                    value=project.get('name', ''),
                    placeholder="E-commerce Platform"
                )
                
                st.text_input(
                    f"Project URL/GitHub", 
                    key=f"proj_url_{i}", 
                    value=project.get('url', ''),
                    placeholder="https://github.com/username/project"
                )
                
                st.text_area(
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
        
        # SUBMIT BUTTON
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

def show_templates():
    st.title("🎨 Resume Templates")
    st.markdown("---")
    
    if 'resume_data' not in st.session_state or not st.session_state.resume_data.get('personal_info', {}).get('name'):
        st.warning("⚠️ Please build your resume first in the 'Build Resume' section!")
        return
    
    st.header("Choose Your Template")
    
    templates = get_all_templates()
    
    # Display templates in columns
    cols = st.columns(3)
    
    for idx, (template_id, template_info) in enumerate(templates.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="border: 2px solid {template_info['color']}; border-radius: 10px; padding: 20px; text-align: center; height: 200px; margin: 10px 0;">
                <h3 style="color: {template_info['color']};">{template_info['name']}</h3>
                <p>{template_info['description']}</p>
                <div style="font-size: 2rem;">{template_info['preview']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {template_info['name']}", key=template_id, use_container_width=True):
                st.session_state.selected_template = template_id
                st.success(f"✅ Selected {template_info['name']} template!")
    
    if st.session_state.get('selected_template'):
        st.info(f"🎯 Current selection: {st.session_state.selected_template}")

def show_preview_ai():
    st.title("👁️ Preview & AI Analysis")
    st.markdown("---")
    
    if 'resume_data' not in st.session_state or not st.session_state.resume_data.get('personal_info', {}).get('name'):
        st.warning("⚠️ Please build your resume first in the 'Build Resume' section!")
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📄 Resume Preview", "🤖 AI Analysis"])
    
    with tab1:
        show_resume_preview()
    
    with tab2:
        show_ai_analysis()

def show_resume_preview():
    st.header("Current Resume Preview")
    
    if st.session_state.get('selected_template'):
        st.success(f"📋 Using template: {st.session_state.selected_template}")
    else:
        st.info("ℹ️ No template selected. Using default format.")
    
    # Display resume data in a nice format
    resume_data = st.session_state.resume_data
    personal_info = resume_data.get('personal_info', {})
    
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {personal_info.get('name', 'N/A')}")
        st.write(f"**Email:** {personal_info.get('email', 'N/A')}")
        st.write(f"**Phone:** {personal_info.get('phone', 'N/A')}")
    
    with col2:
        st.write(f"**Location:** {personal_info.get('location', 'N/A')}")
        if personal_info.get('linkedin'):
            st.write(f"**LinkedIn:** {personal_info.get('linkedin')}")
        if personal_info.get('github'):
            st.write(f"**GitHub:** {personal_info.get('github')}")
    
    st.subheader("📝 Professional Summary")
    st.write(personal_info.get('summary', 'No summary provided'))
    
    # Experience
    if resume_data.get('experience'):
        st.subheader("💼 Work Experience")
        for exp in resume_data['experience']:
            st.write(f"**{exp.get('title', 'N/A')}** at {exp.get('company', 'N/A')}")
            st.write(f"*{exp.get('start_date', 'N/A')} - {exp.get('end_date', 'Present')}*")
            st.write(exp.get('description', 'No description'))
            st.markdown("---")
    
    # Skills
    st.subheader("🛠️ Skills")
    col_tech, col_soft = st.columns(2)
    
    with col_tech:
        if resume_data.get('technical_skills'):
            st.write("**Technical Skills:**")
            for skill in resume_data['technical_skills']:
                st.write(f"• {skill}")
    
    with col_soft:
        if resume_data.get('soft_skills'):
            st.write("**Soft Skills:**")
            for skill in resume_data['soft_skills']:
                st.write(f"• {skill}")

def show_ai_analysis():
    st.header("🤖 AI-Powered Resume Analysis")
    
    if 'ai_analysis' not in st.session_state:
        st.info("💡 Click the button below to generate AI analysis for your resume")
        if st.button("🔄 Generate AI Analysis", type="primary"):
            with st.spinner("🤖 Analyzing your resume with AI..."):
                st.session_state.ai_analysis = get_ai_suggestions(st.session_state.resume_data)
            st.success("✅ AI analysis complete!")
        return
    
    analysis = st.session_state.ai_analysis
    
    # Display ATS Score
    st.subheader("📊 ATS Compatibility Score")
    ats_score = analysis.get('ats_score', 0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Overall Score", f"{ats_score}/100")
    
    with col2:
        # Score indicator
        if ats_score >= 80:
            st.success("🎉 Excellent ATS compatibility!")
        elif ats_score >= 60:
            st.warning("📈 Good, but could be improved")
        else:
            st.error("📝 Needs significant improvement")
    
    # Display suggestions
    st.subheader("💡 AI Suggestions")
    
    suggestions = analysis.get('suggestions', {})
    
    with st.expander("🎯 Overall Improvements", expanded=True):
        for suggestion in suggestions.get('overall_feedback', []):
            st.write(f"• {suggestion}")
    
    with st.expander("🔑 Keyword Optimization"):
        st.info("Consider adding these keywords to improve ATS compatibility:")
        keywords = suggestions.get('missing_keywords', [])
        if keywords:
            cols = st.columns(3)
            for i, keyword in enumerate(keywords[:6]):
                cols[i % 3].warning(f"`{keyword}`")

if __name__ == "__main__":
    main()