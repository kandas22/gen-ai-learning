"""
UI Components - Ultra Premium Clean Design
Sophisticated form with minimal styling
"""

import streamlit as st


def render_input_form():
    """
    Clean, professional input form
    
    Returns:
        Dictionary with form data if submitted, None otherwise
    """
    with st.form("content_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input(
                "📝 Topic / Subject *",
                placeholder="e.g., AI in Healthcare, Sustainable Energy Solutions",
                help="Enter the main topic for content generation"
            )
        
        with col2:
            field = st.selectbox(
                "🎯 Field / Domain *",
                [
                    "Any (General)",
                    "Technology",
                    "Healthcare",
                    "Finance",
                    "Education",
                    "Marketing",
                    "Business",
                    "Science"
                ],
                help="Select target domain"
            )
        
        email = st.text_input(
            "📧 Email (Optional)",
            placeholder="your@email.com",
            help="Receive content via email"
        )
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "🚀 Generate Content",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            return {
                'topic': topic,
                'field': field,
                'email': email
            }
    
    return None