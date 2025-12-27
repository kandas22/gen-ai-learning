"""
SEO Content Generator - Ultra Premium Clean Edition
Sophisticated, minimal design based on user feedback
"""

import streamlit as st
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, Optional

from config import Config
from ui.components import render_input_form
from core.workflow import WorkflowOrchestrator
from utils.helpers import validate_email

# Page configuration
st.set_page_config(
    page_title="AI SEO Content Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra Premium Clean CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #fafbfc;
        padding: 0;
    }
    
    .block-container {
        padding: 1.5rem 3rem 4rem 3rem;
        max-width: 1400px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
    }
    
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
        border: 1.5px solid #e5e7eb;
        padding: 0.625rem 0.875rem;
        font-size: 0.9rem;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 12px;
        padding: 0.25rem;
        border: 1.5px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #6366f1 !important;
        color: white !important;
    }
    
    ::-webkit-scrollbar {width: 8px; height: 8px;}
    ::-webkit-scrollbar-track {background: #f3f4f6;}
    ::-webkit-scrollbar-thumb {background: #d1d5db; border-radius: 4px;}
    ::-webkit-scrollbar-thumb:hover {background: #9ca3af;}
</style>
""", unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Sophisticated Header - Improved space utilization
    st.markdown("""
    <div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 3rem 0 2.5rem 0; margin: -1.5rem -3rem 3rem -3rem; box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);'>
        <div style='max-width: 1400px; margin: 0 auto; padding: 0 3rem;'>
            <div style='text-align: center;'>
                <div style='display: inline-block; background: rgba(255,255,255,0.2); padding: 0.75rem 1.5rem; border-radius: 50px; margin-bottom: 1.5rem; backdrop-filter: blur(10px);'>
                    <span style='color: white; font-weight: 700; font-size: 0.75rem; letter-spacing: 2px;'>AI-POWERED</span>
                </div>
                <h1 style='color: white; margin: 0 0 0.75rem 0; font-weight: 800; font-size: 3rem; letter-spacing: -0.02em;'>SEO Content Generator</h1>
                <p style='color: rgba(255,255,255,0.95); margin: 0; font-size: 1.125rem; font-weight: 500;'>Professional content creation with advanced AI • Optimized • Production-ready</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Validate config
    is_valid, error_msg = Config.validate()
    if not is_valid:
        st.error(f"⚠️ Configuration Error: {error_msg}")
        st.info("💡 Check your .env file for API keys")
        st.stop()

    # Informational notes (non-fatal), e.g. SMTP optional
    if error_msg:
        st.info(f"⚠️ Configuration: {error_msg}")
    
    # Initialize session state
    init_session_state()
    
    # Input Form
    form_data = render_input_form()
    
    # Process form submission FIRST (before showing progress)
    if form_data and not st.session_state.get('workflow_continue'):
        # New workflow starting
        topic = form_data['topic']
        field = form_data['field']
        recipient_email = form_data.get('email')
        
        if not topic or len(topic.strip()) < 5:
            st.error("⚠️ Please enter a topic (minimum 5 characters)")
            st.stop()
        
        if recipient_email and not validate_email(recipient_email):
            st.error("⚠️ Please enter a valid email address")
            st.stop()
        
        reset_workflow_state(recipient_email)
        run_workflow(topic, field, recipient_email)
        # After workflow, st.rerun() is called, so execution stops here
    
    # Clear workflow_continue flag after form is shown again
    if 'workflow_continue' in st.session_state:
        del st.session_state.workflow_continue
    
    # ALWAYS show progress dashboard - will show after form submission or on page load
    show_progress()
    
    # Show results after workflow completes
    if st.session_state.get('results'):
        display_results(st.session_state.results)


def init_session_state():
    """Initialize session state"""
    defaults = {
        'workflow_step': 0,
        'current_agent_name': None,
        'completed_steps': [],
        'workflow_running': False,
        'progress_visible': False,
        'email_provided': False,
        'workflow_started': False,
        'total_steps': 4,  # Fixed per run, updated in reset_workflow_state
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_workflow_state(email: Optional[str]):
    """Reset workflow state"""
    st.session_state.workflow_step = 0
    st.session_state.current_agent_name = None
    st.session_state.completed_steps = []
    st.session_state.workflow_running = True
    st.session_state.progress_visible = True
    st.session_state.email_provided = bool(email and email.strip())
    st.session_state.workflow_started = True
    
    # Fix total_steps ONCE per run
    st.session_state.total_steps = 5 if st.session_state.email_provided else 4
    
    if 'results' in st.session_state:
        del st.session_state.results


def show_progress():
    """Clean, sophisticated progress dashboard - recreates UI every time"""
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    
    # Get data
    agents = [
        ("Research Agent", "🔍", "#3b82f6"),
        ("Content Agent", "✍️", "#8b5cf6"),
        ("Verification Agent", "✅", "#10b981"),
        ("SEO Agent", "📊", "#f59e0b"),
        ("Email Agent", "📧", "#ec4899")  # Always include
    ]
    
    # Use total_steps from session state (fixed per run)
    total_steps = st.session_state.get('total_steps', 4)
    current_step = st.session_state.workflow_step
    
    # Show only relevant agents
    if st.session_state.email_provided:
        visible_agents = agents  # All 5
    else:
        visible_agents = agents[:-1]  # First 4 only
    
    # Calculate percentage based on completed steps count
    percentage = int((current_step / total_steps) * 100) if total_steps > 0 else 0
    
    agent_to_step = {
        "Research Agent": "research",
        "Content Agent": "content",
        "Verification Agent": "verification",
        "SEO Agent": "seo_scoring",
        "Email Agent": "email_delivery"
    }
    
    # Recreate columns every time (DO NOT store in session_state)
    col1, col2 = st.columns([1, 2], gap="large")
    
    # Determine status text
    if not st.session_state.get('workflow_started', False):
        status_text = "Ready"
        status_color = "#6b7280"
    elif st.session_state.workflow_running:
        status_text = "Processing"
        status_color = "#f59e0b"
    else:
        status_text = "Completed"
        status_color = "#10b981"
    
    # Progress Metrics
    with col1:
        st.markdown(f"""
<div style='background: white; padding: 2rem; border-radius: 16px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
<div style='text-align: center; margin-bottom: 2rem;'>
<div style='width: 150px; height: 150px; margin: 0 auto; border-radius: 50%; background: conic-gradient(#6366f1 0% {percentage}%, #f3f4f6 {percentage}% 100%); padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);'>
<div style='width: 100%; height: 100%; border-radius: 50%; background: white; display: flex; flex-direction: column; align-items: center; justify-content: center;'>
<div style='font-size: 2.5rem; font-weight: 800; color: #6366f1;'>{percentage}%</div>
<div style='font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem; font-weight: 600;'>Complete</div>
</div>
</div>
</div>
<div style='background: #f9fafb; padding: 1.25rem; border-radius: 12px; border: 1px solid #e5e7eb;'>
<div style='margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #e5e7eb;'>
<div style='color: #9ca3af; font-size: 0.7rem; margin-bottom: 0.35rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Progress</div>
<div style='font-size: 1.125rem; font-weight: 700; color: #111827;'>{current_step} / {total_steps} Steps</div>
</div>
<div>
<div style='color: #9ca3af; font-size: 0.7rem; margin-bottom: 0.35rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Status</div>
<div style='font-size: 0.95rem; font-weight: 700; color: {status_color};'>{"✅" if status_text == "Completed" else "⏳" if status_text == "Processing" else "⭕"} {status_text}</div>
</div>
</div>
</div>
        """, unsafe_allow_html=True)
    
    # Agent Status
    with col2:
        agent_cards_html = ""
        
        for idx, (agent_name, icon, color) in enumerate(visible_agents):
            step_name_internal = agent_to_step.get(agent_name, "")
            
            if step_name_internal in st.session_state.completed_steps:
                # Completed
                agent_cards_html += f"""
<div style='background: white; padding: 1.25rem 1.5rem; margin: 0.75rem 0; border-radius: 12px; border-left: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; align-items: center; gap: 1rem;'>
<div style='width: 50px; height: 50px; background: {color}10; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;'>{icon}</div>
<div style='flex: 1;'>
<div style='font-weight: 700; color: #111827; font-size: 0.95rem;'>{agent_name}</div>
<div style='font-size: 0.8rem; color: {color}; margin-top: 0.25rem; font-weight: 600;'>✅ Completed</div>
</div>
<div style='width: 10px; height: 10px; background: {color}; border-radius: 50%;'></div>
</div>
"""
            elif st.session_state.current_agent_name and agent_name == st.session_state.current_agent_name:
                # In Progress - exact name match now works!
                agent_cards_html += f"""
<div style='background: white; padding: 1.25rem 1.5rem; margin: 0.75rem 0; border-radius: 12px; border-left: 4px solid {color}; box-shadow: 0 4px 16px rgba(99,102,241,0.2); display: flex; align-items: center; gap: 1rem; animation: borderPulse 2s infinite;'>
<div style='width: 50px; height: 50px; background: {color}15; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;'>{icon}</div>
<div style='flex: 1;'>
<div style='font-weight: 700; color: #111827; font-size: 0.95rem;'>{agent_name}</div>
<div style='font-size: 0.8rem; color: {color}; margin-top: 0.25rem; font-weight: 600;'>⏳ In Progress</div>
</div>
<div style='width: 10px; height: 10px; background: {color}; border-radius: 50%; animation: pulse 2s infinite;'></div>
</div>
"""
            else:
                # Pending
                if st.session_state.get('workflow_started', False):
                    pending_text = "In Pipeline"
                    pending_icon = "⏸️"
                else:
                    pending_text = "Waiting to Begin"
                    pending_icon = "⭕"
                
                agent_cards_html += f"""
<div style='background: #f9fafb; padding: 1.25rem 1.5rem; margin: 0.75rem 0; border-radius: 12px; border-left: 4px solid #e5e7eb; display: flex; align-items: center; gap: 1rem; opacity: 0.6;'>
<div style='width: 50px; height: 50px; background: #f3f4f6; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; opacity: 0.5;'>{icon}</div>
<div style='flex: 1;'>
<div style='font-weight: 700; color: #6b7280; font-size: 0.95rem;'>{agent_name}</div>
<div style='font-size: 0.8rem; color: #9ca3af; margin-top: 0.25rem; font-weight: 600;'>{pending_icon} {pending_text}</div>
</div>
<div style='width: 10px; height: 10px; background: #d1d5db; border-radius: 50%;'></div>
</div>
"""
        
        st.markdown(f"""
<div style='background: white; padding: 1.5rem; border-radius: 16px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
<div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;'>
<h3 style='margin: 0; color: #111827; font-size: 1.125rem; font-weight: 700;'>AI Agent Status</h3>
<div style='padding: 0.375rem 0.875rem; background: #f3f4f6; border-radius: 20px; font-size: 0.75rem; font-weight: 700; color: #6b7280;'>{current_step}/{total_steps}</div>
</div>
{agent_cards_html}
</div>
        """, unsafe_allow_html=True)
    
    # Animations
    st.markdown("""
<style>
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}
@keyframes borderPulse {
    0%, 100% { box-shadow: 0 4px 16px rgba(99,102,241,0.2); }
    50% { box-shadow: 0 4px 20px rgba(99,102,241,0.35); }
}
</style>
    """, unsafe_allow_html=True)


def run_workflow(topic: str, field: str, email: Optional[str] = None):
    """Execute workflow with live step-by-step status using st.status()"""
    
    AGENT_NAME_MAP = {
        "research": "Research Agent",
        "content": "Content Agent",
        "verification": "Verification Agent",
        "seo_scoring": "SEO Agent",
        "email_delivery": "Email Agent"
    }
    
    # Create status placeholders for each step
    status_updates = {}
    
    def update_status(step: str, status: str, message: str = ""):
        """Update session state and status display"""
        agent_name = AGENT_NAME_MAP.get(step, "")
        st.session_state.current_agent_name = agent_name
        
        if status == "running":
            # Update status display
            if step in status_updates:
                status_updates[step].update(label=f"⏳ {agent_name}", state="running")
        
        elif status == "completed":
            if step not in st.session_state.completed_steps:
                st.session_state.completed_steps.append(step)
            st.session_state.workflow_step = len(st.session_state.completed_steps)
            
            # Update status display
            if step in status_updates:
                status_updates[step].update(label=f"✅ {agent_name}", state="complete")
    
    try:
        # Create main status container with expandable steps
        with st.status("🚀 Generating content...", expanded=True) as main_status:
            # Create status containers for each step
            workflow_steps = ["research", "content", "verification", "seo_scoring"]
            if st.session_state.email_provided:
                workflow_steps.append("email_delivery")
            
            for step in workflow_steps:
                agent_name = AGENT_NAME_MAP[step]
                status_updates[step] = st.status(f"⏸️ {agent_name}", expanded=False)
            
            # Execute workflow
            orchestrator = WorkflowOrchestrator(status_callback=update_status)
            
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            try:
                results = loop.run_until_complete(
                    orchestrator.execute_workflow(
                        topic=topic,
                        field=field,
                        recipient_email=email
                    )
                )
            except RuntimeError as e:
                if "cannot be called from a running event loop" in str(e):
                    try:
                        import nest_asyncio
                        nest_asyncio.apply()
                        results = asyncio.run(
                            orchestrator.execute_workflow(
                                topic=topic,
                                field=field,
                                recipient_email=email
                            )
                        )
                    except ImportError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        results = loop.run_until_complete(
                            orchestrator.execute_workflow(
                                topic=topic,
                                field=field,
                                recipient_email=email
                            )
                        )
                else:
                    raise
            
            # Update main status
            main_status.update(label="✅ Content generation complete!", state="complete", expanded=False)
        
        # Store results
        st.session_state.results = results
        st.session_state.workflow_running = False
        
        # Set all steps as completed
        completed_list = ["research", "content", "verification", "seo_scoring"]
        if st.session_state.email_provided:
            completed_list.append("email_delivery")
        
        st.session_state.completed_steps = completed_list
        st.session_state.workflow_step = len(completed_list)
        
        # Show completion
        if results.get('status') == 'completed':
            st.success("🎉 Content generation completed successfully!")
            st.balloons()
        else:
            st.warning("⚠️ Workflow completed with some issues")
        
        # Mark that we should continue (not restart) on next rerun
        st.session_state.workflow_continue = True
        
        # Rerun to show final state
        st.rerun()
    
    except Exception as e:
        st.session_state.workflow_running = False
        st.error(f"❌ Workflow failed: {str(e)}")
        st.exception(e)


def display_results(results: Dict[str, Any]):
    """Clean results display with unique colored boxes"""
    
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Compact metrics with unique colors
    status = results.get('status', 'Unknown')
    seo_data = results.get('seo_score', {})
    score = 0
    if isinstance(seo_data, dict) and 'raw_data' in seo_data:
        score = seo_data['raw_data'].get('percentage', 0)
    
    content = results.get('generated_content', '')
    word_count = len(content.split()) if content else 0
    reading_time = max(1, word_count // 200)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Unique colors for each metric
    metrics = [
        (col1, "✅", "Status", status.upper(), "#10b981", "#d1fae5"),
        (col2, "📊", "SEO Score", f"{score}%", "#6366f1", "#e0e7ff"),
        (col3, "📝", "Words", f"{word_count:,}", "#ec4899", "#fce7f3"),
        (col4, "⏱️", "Read Time", f"{reading_time}m", "#f59e0b", "#fef3c7")
    ]
    
    for col, icon, label, value, color, bg in metrics:
        with col:
            st.markdown(f"""
<div style='background: {bg}; padding: 1.125rem; border-radius: 12px; text-align: center; border: 2px solid {color}30; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
<div style='font-size: 1.625rem; margin-bottom: 0.5rem;'>{icon}</div>
<div style='color: #6b7280; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;'>{label}</div>
<div style='color: {color}; font-size: 1.375rem; font-weight: 800;'>{value}</div>
</div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs(["📄 Overview", "🔍 Research", "📝 Content", "✅ Verification", "📊 SEO Analysis"])
    
    with tabs[0]:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
<h4 style='margin: 0 0 1rem 0; color: #111827; font-size: 0.95rem; font-weight: 700;'>📊 Statistics</h4>
<div style='line-height: 1.8; font-size: 0.9rem;'>
<div><span style='color: #9ca3af;'>Words:</span> <strong>{word_count:,}</strong></div>
<div><span style='color: #9ca3af;'>SEO Score:</span> <strong>{score}%</strong></div>
<div><span style='color: #9ca3af;'>Status:</span> <strong>{status}</strong></div>
</div>
</div>
            """, unsafe_allow_html=True)
        
        with col_b:
            quality = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Work"
            st.markdown(f"""
<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
<h4 style='margin: 0 0 1rem 0; color: #111827; font-size: 0.95rem; font-weight: 700;'>🎯 Quality</h4>
<div style='line-height: 1.8; font-size: 0.9rem;'>
<div><span style='color: #9ca3af;'>Overall:</span> <strong>{quality}</strong></div>
<div><span style='color: #9ca3af;'>Optimization:</span> <strong>{'Optimized' if score >= 70 else 'Needs Work'}</strong></div>
<div><span style='color: #9ca3af;'>Read Time:</span> <strong>~{reading_time} min</strong></div>
</div>
</div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        research = results.get('research_output', '')
        if research:
            st.markdown(f"<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>{research}</div>", unsafe_allow_html=True)
        else:
            st.info("No research data available")
    
    with tabs[2]:
        if content:
            st.markdown(f"<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>{content}</div>", unsafe_allow_html=True)
            st.download_button(
                "📥 Download Content",
                content,
                f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                "text/markdown",
                use_container_width=True
            )
        else:
            st.info("No content generated")
    
    with tabs[3]:
        verification = results.get('verification_output', '')
        if verification:
            st.markdown(f"<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>{verification}</div>", unsafe_allow_html=True)
        else:
            st.info("No verification data")
    
    with tabs[4]:
        seo_output = results.get('seo_score', {})
        if seo_output and 'analysis' in seo_output:
            st.markdown(f"<div style='background: white; padding: 1.5rem; border-radius: 12px; border: 1.5px solid #e5e7eb; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>{seo_output['analysis']}</div>", unsafe_allow_html=True)
        else:
            st.info("No SEO analysis available")
        
        if score > 0:
            st.progress(score / 100)


if __name__ == "__main__":
    main()