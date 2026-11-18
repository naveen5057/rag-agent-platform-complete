import streamlit as st
import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime

# Configuration
# AGENT_SERVICE_URL = "http://localhost:8000"
# MCP_SERVER_URL = "http://localhost:8080"

#configuration for docker
AGENT_SERVICE_URL = "http://agent-service:8000"
MCP_SERVER_URL = "http://mcp-server:8080"

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "service_status" not in st.session_state:
    st.session_state.service_status = {
        "agent_service": None,
        "mcp_server": None
    }

def check_services():
    """Check if backend services are running."""
    status = {"agent_service": False, "mcp_server": False}
    
    try:
        # Check Agent Service
        response = requests.get(f"{AGENT_SERVICE_URL}/health", timeout=3)
        if response.status_code == 200:
            status["agent_service"] = True
            st.session_state.agent_info = response.json()
    except:
        pass
    
    try:
        # Check MCP Server (might not have health endpoint, check connection)
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=3)
        if response.status_code < 500:
            status["mcp_server"] = True
    except:
        pass
    
    st.session_state.service_status = status
    return status

def query_agent(question: str) -> Optional[Dict]:
    """Send question to agent service."""
    try:
        payload = {"question": question}
        response = requests.post(
            f"{AGENT_SERVICE_URL}/agent/query",
            json=payload,
            timeout=30  # Longer timeout for agent processing
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Agent service error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to agent service. Make sure it's running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The agent may be taking too long to process.")
        return None
    except Exception as e:
        st.error(f"Error querying agent: {str(e)}")
        return None

def format_timestamp() -> str:
    """Format current timestamp."""
    return datetime.now().strftime("%H:%M:%S")

# Streamlit app layout
st.set_page_config(
    page_title="RAG Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Agent Platform")
    st.markdown("---")
    
    # Service status
    st.subheader("Service Status")
    
    status = check_services()
    
    agent_status = "🟢 Running" if status["agent_service"] else "🔴 Stopped"
    mcp_status = "🟢 Running" if status["mcp_server"] else "🔴 Stopped"
    
    st.write(f"**Agent Service:** {agent_status}")
    st.write(f"**MCP Server:** {mcp_status}")
    
    if status["agent_service"] and "agent_info" in st.session_state:
        agent_info = st.session_state.agent_info
        st.write(f"**Mode:** {agent_info.get('mode', 'N/A')}")
        st.write(f"**Tools Available:** {len(agent_info.get('mcp_tools', []))}")
    
    st.markdown("---")
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.last_response = None
        st.rerun()
    
    # Debug info
    with st.expander("Debug Information"):
        st.write(f"Agent Service URL: `{AGENT_SERVICE_URL}`")
        st.write(f"MCP Server URL: `{MCP_SERVER_URL}`")
        
        if st.button("Test Connection"):
            status = check_services()
            if all(status.values()):
                st.success("✅ All services connected!")
            else:
                st.error("❌ Some services are not available")
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This UI allows you to interact with the RAG Agent Platform.
    
    **Features:**
    - Ask questions to the AI agent
    - View conversation history
    - See which tools were used
    - Monitor service status
    
    **Backend Services:**
    - Agent Service (Port 8000)
    - MCP Server (Port 8080)
    - Mock RAG API (Port 9000)
    - Mock Pipeline API (Port 9001)
    """)

# Main content area
st.title("💬 RAG Agent Interface")
st.markdown("Ask questions and interact with the AI agent powered by your RAG platform.")

# Two-column layout for chat
col1, col2 = st.columns([2, 1])

with col1:
    # Question input
    question = st.text_input(
        "Ask a question:",
        placeholder="Type your question here...",
        key="question_input"
    )
    
    # Submit button
    submit_col1, submit_col2 = st.columns([1, 4])
    with submit_col1:
        submit_btn = st.button("🚀 Submit", use_container_width=True)
    
    # Process question when submitted
    if submit_btn and question:
        with st.spinner("🤔 Processing your question..."):
            # Add user message to conversation
            st.session_state.conversation_history.append({
                "role": "user",
                "content": question,
                "timestamp": format_timestamp()
            })
            
            # Query agent
            response = query_agent(question)
            
            if response:
                # Add agent response to conversation
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response.get("answer", "No answer received"),
                    "tools_used": response.get("tools_used", []),
                    "timestamp": format_timestamp()
                })
                
                # Store last response for detailed view
                st.session_state.last_response = response
                
                # Rerun to update the display
                st.rerun()
            else:
                st.error("Failed to get response from agent.")

    # Conversation history
    st.markdown("---")
    st.subheader("Conversation History")
    
    if not st.session_state.conversation_history:
        st.info("No conversation yet. Ask a question to get started!")
    else:
        # Display conversation in reverse chronological order (newest first)
        for message in reversed(st.session_state.conversation_history):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"**You** ({message['timestamp']}):")
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**Assistant** ({message['timestamp']}):")
                    st.write(message["content"])
                    
                    # Show tools used if available
                    if message.get("tools_used"):
                        tools_text = ", ".join(message["tools_used"])
                        st.caption(f"🔧 Tools used: {tools_text}")
            
            st.markdown("---")

with col2:
    # Detailed response view
    st.subheader("📊 Response Details")
    
    if st.session_state.last_response:
        response = st.session_state.last_response
        
        # Answer
        st.markdown("### Answer")
        st.info(response.get("answer", "No answer received"))
        
        # Tools used
        tools_used = response.get("tools_used", [])
        st.markdown("### Tools Used")
        if tools_used:
            for tool in tools_used:
                st.success(f"✅ {tool}")
        else:
            st.warning("No tools were used for this response")
        
        # Raw JSON view
        with st.expander("View Raw Response"):
            st.json(response)
    else:
        st.info("Submit a question to see response details here.")
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    if st.button("🔄 Check Service Health", use_container_width=True):
        status = check_services()
        if all(status.values()):
            st.success("All services are running!")
        else:
            st.error("Some services are not available")
        st.rerun()
    
    # Example questions
    st.markdown("---")
    st.subheader("💡 Example Questions")
    
    example_questions = [
        "What is the ingestion process for documents?",
        "Check the status of pipeline execution ABC123",
        "How does the RAG system work?",
        "What tools are available in the MCP server?"
    ]
    
    for example in example_questions:
        if st.button(example, use_container_width=True):
            st.session_state.question_input = example
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    RAG Agent Platform UI • Built with Streamlit • Agent Service running on port 8000
    </div>
    """,
    unsafe_allow_html=True
)