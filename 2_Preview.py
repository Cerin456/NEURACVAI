import streamlit as st
from utils.template_engine import render_template, get_all_templates
from utils.ai_suggestions import get_ai_suggestions

def show_preview():
    st.title("👁️ Resume Preview & AI Analysis")
    st.markdown("---")
    
    if 'resume_data' not in st.session_state or not st.session_state.resume_data:
        st.warning("⚠️ Please build your resume first in the 'Build Resume' section!")
        return
    
    # Create tabs
    tab1, tab2 = st.tabs(["📄 Resume Preview", "🤖 AI Analysis"])
    
    with tab1:
        show_resume_preview()
    
    with tab2:
        show_ai_analysis()

def show_resume_preview():
    st.header("Current Resume Preview")
    
    # Template selection
    templates = get_all_templates()
    selected_template = st.selectbox(
        "Choose Template",
        options=list(templates.keys()),
        format_func=lambda x: templates[x]['name'],
        key="preview_template"
    )
    
    # Display resume
    html_content = render_template(selected_template, st.session_state.resume_data)
    st.components.v1.html(html_content, height=800, scrolling=True)
    
    # Download option
    st.download_button(
        label="📄 Download HTML Resume",
        data=html_content,
        file_name="resume.html",
        mime="text/html"
    )

def show_ai_analysis():
    st.header("🤖 AI-Powered Resume Analysis")
    
    if st.button("🔄 Analyze Resume with AI", type="primary"):
        with st.spinner("Analyzing your resume with AI..."):
            st.session_state.ai_analysis = get_ai_suggestions(st.session_state.resume_data)
    
    if 'ai_analysis' not in st.session_state:
        st.info("Click the button above to get AI suggestions for your resume")
        return
    
    analysis = st.session_state.ai_analysis
    
    # Display ATS Score
    st.metric("ATS Score", f"{analysis.get('ats_score', 0)}/100")
    
    # Display suggestions
    st.subheader("💡 AI Suggestions")
    suggestions = analysis.get('suggestions', {})
    
    for suggestion in suggestions.get('overall_feedback', []):
        st.write(f"• {suggestion}")

if __name__ == "__main__":
    show_preview()