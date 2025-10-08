import streamlit as st

def show_templates():
    st.title("🎨 Choose Your Template")
    st.markdown("---")
    
    if 'resume_data' not in st.session_state:
        st.warning("Please build your resume first!")
        if st.button("Go to Build Resume"):
            st.switch_page("pages/1_Build_Resume.py")
        return
    
    templates = {
        'template1': {'name': 'Professional', 'description': 'Clean design'},
        'template2': {'name': 'Modern', 'description': 'Contemporary style'},
        'template3': {'name': 'Creative', 'description': 'Creative layout'}
    }
    
    cols = st.columns(3)
    for idx, (template_id, template_info) in enumerate(templates.items()):
        col = cols[idx % 3]
        with col:
            st.subheader(template_info['name'])
            st.caption(template_info['description'])
            if st.button(f"Select {template_info['name']}", key=template_id):
                st.session_state.selected_template = template_id
                st.success(f"Selected {template_info['name']}!")
    
    if st.session_state.get('selected_template'):
        st.info(f"Selected template: {st.session_state.selected_template}")
        if st.button("👁️ View Preview"):
            st.switch_page("pages/3_Preview.py")

if __name__ == "__main__":
    show_templates()