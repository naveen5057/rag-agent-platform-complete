#!/usr/bin/env python3
"""Test integration between Streamlit UI and Agent Service."""

import requests
import json
import time

def test_agent_service():
    """Test if agent service is responding."""
    print("Testing Agent Service connection...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Service is running:")
            print(f"   Mode: {data.get('mode', 'N/A')}")
            print(f"   Tools: {len(data.get('mcp_tools', []))}")
            print(f"   Status: {data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Agent Service returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Agent Service on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mcp_server():
    """Test if MCP server is responding."""
    print("\nTesting MCP Server connection...")
    
    try:
        # Try health endpoint first
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code < 500:
            print(f"✅ MCP Server is responding (status: {response.status_code})")
            return True
        else:
            print(f"⚠️  MCP Server returned status: {response.status_code}")
            # Still consider it running if we get any response
            return response.status_code < 500
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to MCP Server on port 8080")
        return False
    except Exception as e:
        print(f"⚠️  MCP Server check: {e}")
        return False

def test_agent_query():
    """Test sending a query to the agent."""
    print("\nTesting agent query...")
    
    test_question = "What is the ingestion process?"
    
    try:
        payload = {"question": test_question}
        response = requests.post(
            "http://localhost:8000/agent/query",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent query successful!")
            print(f"   Answer: {data.get('answer', 'N/A')[:100]}...")
            print(f"   Tools used: {data.get('tools_used', [])}")
            return True
        else:
            print(f"❌ Agent query failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Agent Service for query")
        return False
    except requests.exceptions.Timeout:
        print("❌ Agent query timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_streamlit_ui():
    """Test if Streamlit UI can be started."""
    print("\nTesting Streamlit UI setup...")
    
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
        
        # Check if the app file exists
        import os
        if os.path.exists("streamlit-ui/app.py"):
            print("✅ Streamlit app file found")
            return True
        else:
            print("❌ Streamlit app file not found")
            return False
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("RAG Agent Platform Integration Test")
    print("=" * 60)
    
    print("\nMake sure the backend services are running:")
    print("1. Mock RAG API (port 9000)")
    print("2. Mock Pipeline API (port 9001)")
    print("3. MCP Server (port 8080)")
    print("4. Agent Service (port 8000)")
    
    print("\nYou can start them using:")
    print("  - VS Code debug configuration 'Complete Platform with UI'")
    print("  - Or individually using the debug configurations")
    
    print("\n" + "=" * 60)
    
    # Run tests
    all_tests_passed = True
    
    # Test Streamlit setup
    if not test_streamlit_ui():
        all_tests_passed = False
    
    # Test backend services
    if not test_agent_service():
        all_tests_passed = False
    
    if not test_mcp_server():
        all_tests_passed = False
    
    # Test agent query (only if services are running)
    if all_tests_passed:
        if not test_agent_query():
            all_tests_passed = False
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("🎉 All tests passed! The platform is ready.")
        print("\nTo start the Streamlit UI:")
        print("1. In VS Code, select 'Streamlit UI' debug configuration")
        print("2. Press F5 to start")
        print("3. Open browser to: http://localhost:8501")
        print("\nOr run from terminal:")
        print("  streamlit run streamlit-ui/app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting steps:")
        print("1. Make sure all services are running")
        print("2. Check that dependencies are installed: pip install -r requirements-dev.txt")
        print("3. Verify ports are not in use")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()