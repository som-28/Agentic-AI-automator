"""Streamlit GUI for Personal Task Automation Agent.

Provides a user-friendly interface for:
- Task execution with natural language commands
- Resume upload and analysis
- Job matching based on resume
- Execution history tracking
"""
try:
    import streamlit as st
except ImportError:
    print("Streamlit not installed. Please run: pip install streamlit")
    exit(1)

import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.planner import Planner as RulePlanner
from src.agent.planner_llm import LLMPlanner
from src.agent.controller import Controller
from src.utils.config import load_config


# Page configuration
st.set_page_config(
    page_title="Task Automation Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = None
if "job_results" not in st.session_state:
    st.session_state.job_results = None


def get_planner_mode():
    """Get the current planner mode from config."""
    cfg = load_config()
    return cfg.get("PLANNER_MODE", "rule")


def execute_command_async(command: str, email: Optional[str] = None):
    """Execute a command using the agent."""
    try:
        cfg = load_config()
        planner_mode = get_planner_mode()
        
        # Choose planner
        if planner_mode == "llm" and cfg.get("OPENAI_API_KEY"):
            planner = LLMPlanner(cfg)
        else:
            planner = RulePlanner(cfg)
        
        # Create plan
        plan = planner.plan(command, email)
        
        # Execute plan
        controller = Controller(cfg, use_enhanced=True)
        
        # Run async execution
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        logs = loop.run_until_complete(controller.execute_plan(plan))
        loop.close()
        
        return {
            "success": True,
            "plan": plan,
            "logs": logs,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def main():
    # Header
    st.markdown('<div class="main-header">🤖 Personal Task Automation Agent</div>', unsafe_allow_html=True)
    
    # Sidebar with configuration info
    with st.sidebar:
        st.header("⚙️ Configuration")
        cfg = load_config()
        
        planner_mode = get_planner_mode()
        st.info(f"**Planner Mode:** {planner_mode.upper()}")
        
        st.subheader("API Status")
        if cfg.get("OPENAI_API_KEY"):
            st.success("✅ OpenAI API")
        else:
            st.warning("⚠️ OpenAI API (using fallback)")
        
        if cfg.get("SERPAPI_KEY"):
            st.success("✅ SerpAPI")
        else:
            st.warning("⚠️ SerpAPI (using demo mode)")
        
        if cfg.get("SMTP_HOST"):
            st.success("✅ SMTP Email")
        else:
            st.warning("⚠️ Email (demo mode)")
        
        st.markdown("---")
        st.subheader("📚 Quick Help")
        st.markdown("""
        **Task Examples:**
        - "Search for AI news and email me summary"
        - "Find Python tutorials and summarize"
        - "Scrape https://example.com"
        
        **Resume Analysis:**
        - Upload PDF/DOCX/TXT resume
        - Get AI-powered analysis
        - Find matching jobs
        """)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🚀 Task Execution", "📄 Resume Analysis", "📜 History"])
    
    # ========== Tab 1: Task Execution ==========
    with tab1:
        st.header("Natural Language Task Execution")
        st.markdown("Enter a command in natural language and let the agent handle it.")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            command = st.text_area(
                "Command",
                placeholder="e.g., Search for latest AI news and email me a summary",
                height=100,
                key="task_command"
            )
        with col2:
            email = st.text_input(
                "Email (optional)",
                placeholder="your@email.com",
                key="task_email"
            )
        
        if st.button("🚀 Execute Task", type="primary", use_container_width=True):
            if not command.strip():
                st.error("Please enter a command")
            else:
                with st.spinner("Executing task..."):
                    result = execute_command_async(command, email if email.strip() else None)
                    
                    # Add to history
                    st.session_state.history.insert(0, {
                        "command": command,
                        "result": result,
                        "type": "task"
                    })
                    
                    if result["success"]:
                        st.markdown('<div class="success-box">✅ Task completed successfully!</div>', unsafe_allow_html=True)
                        
                        with st.expander("📋 Plan Details"):
                            st.json(result["plan"])
                        
                        with st.expander("📝 Execution Logs"):
                            for log in result["logs"]:
                                st.text(log)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
    
    # ========== Tab 2: Resume Analysis ==========
    with tab2:
        st.header("Resume Analysis & Job Matching")
        st.markdown("Upload your resume to get AI-powered analysis and find matching jobs.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Resume")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["pdf", "docx", "txt"],
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if uploaded_file:
                st.success(f"Uploaded: {uploaded_file.name}")
                
                if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
                    with st.spinner("Analyzing resume..."):
                        try:
                            # Save uploaded file temporarily
                            temp_path = os.path.join("temp", uploaded_file.name)
                            os.makedirs("temp", exist_ok=True)
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Parse resume
                            from src.tools.resume_parser_tool import run as parse_resume
                            parse_logs, parse_output = parse_resume({"file_path": temp_path}, {})
                            
                            if "error" in parse_output:
                                st.error(f"Parse error: {parse_output['error']}")
                            else:
                                # Analyze resume
                                from src.tools.resume_analyzer_tool import run as analyze_resume
                                context = {"resume_data": parse_output}
                                analyze_logs, analyze_output = analyze_resume({}, context)
                                
                                if "error" in analyze_output:
                                    st.error(f"Analysis error: {analyze_output['error']}")
                                else:
                                    st.session_state.resume_analysis = {
                                        "parse": parse_output,
                                        "analysis": analyze_output["analysis"],
                                        "file_name": uploaded_file.name
                                    }
                                    st.success("✅ Resume analyzed successfully!")
                            
                            # Cleanup
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        with col2:
            st.subheader("📊 Analysis Results")
            
            if st.session_state.resume_analysis:
                analysis = st.session_state.resume_analysis["analysis"]
                
                st.markdown("**Candidate Information:**")
                if analysis.get("name"):
                    st.info(f"**Name:** {analysis['name']}")
                
                if analysis.get("field_of_study"):
                    st.info(f"**Field:** {analysis['field_of_study']}")
                
                if analysis.get("experience_years"):
                    st.info(f"**Experience:** {analysis['experience_years']} years")
                
                if analysis.get("skills"):
                    st.markdown("**Skills:**")
                    st.write(", ".join(analysis["skills"]))
                
                if analysis.get("career_interests"):
                    st.markdown("**Career Interests:**")
                    st.write(", ".join(analysis["career_interests"]))
                
                # Job search section
                st.markdown("---")
                st.subheader("🔍 Find Matching Jobs")
                
                location = st.text_input("Location", value="remote", key="job_location")
                num_results = st.slider("Number of results", 5, 20, 10, key="job_limit")
                
                if st.button("🎯 Search Jobs", type="primary", use_container_width=True):
                    with st.spinner("Searching for jobs..."):
                        try:
                            from src.tools.job_matcher_tool import run as search_jobs
                            context = {"resume_analysis": {"analysis": analysis}}
                            job_args = {"location": location, "limit": num_results}
                            job_logs, job_output = search_jobs(job_args, context)
                            
                            if "error" in job_output:
                                st.error(f"Search error: {job_output['error']}")
                            else:
                                st.session_state.job_results = job_output
                                st.success(f"✅ Found {len(job_output['job_matches'])} results!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("Upload and analyze a resume to see results here.")
        
        # Display job results
        if st.session_state.job_results:
            st.markdown("---")
            st.subheader("💼 Job Matches")
            
            jobs = st.session_state.job_results["job_matches"]
            query = st.session_state.job_results.get("search_query", "")
            
            st.info(f"**Search Query:** {query}")
            
            for i, job in enumerate(jobs, 1):
                with st.expander(f"{i}. {job['title']} ({job['relevance']} relevance)"):
                    st.markdown(f"**URL:** [{job['url']}]({job['url']})")
                    st.markdown(f"**Description:** {job['snippet']}")
                    if job.get("matched_skills"):
                        st.markdown(f"**Matched Skills:** {', '.join(job['matched_skills'])}")
    
    # ========== Tab 3: History ==========
    with tab3:
        st.header("Execution History")
        
        if not st.session_state.history:
            st.info("No execution history yet. Start by executing a task or analyzing a resume.")
        else:
            if st.button("🗑️ Clear History", key="clear_history"):
                st.session_state.history = []
                st.rerun()
            
            st.markdown(f"**Total Executions:** {len(st.session_state.history)}")
            
            for i, item in enumerate(st.session_state.history, 1):
                with st.expander(f"{i}. {item.get('command', 'Resume Analysis')} - {item['result'].get('timestamp', '')}"):
                    if item["type"] == "task":
                        if item["result"]["success"]:
                            st.success("✅ Successful")
                            st.json(item["result"]["plan"])
                            st.text("Logs:")
                            for log in item["result"]["logs"]:
                                st.text(log)
                        else:
                            st.error(f"❌ Failed: {item['result']['error']}")
                    else:
                        st.json(item["result"])


if __name__ == "__main__":
    main()
