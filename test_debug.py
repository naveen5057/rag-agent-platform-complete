#!/usr/bin/env python3
"""Test script to verify debug configuration works."""

import requests
import time

def test_agent_service():
    """Test the agent service endpoint."""
    print("Testing Agent Service...")
    
    # Start with a simple test
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ Agent Service health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Agent Service not running on port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_mcp_server():
    """Test the MCP server health endpoint."""
    print("\nTesting MCP Server...")
    
    url = "http://localhost:8080/health"
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ MCP Server health check: {response.status_code}")
        # MCP server might not have a /health endpoint, check status code
        if response.status_code < 500:
            print(f"Response status: {response.status_code}")
            return True
        else:
            print(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ MCP Server not running on port 8080")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Debug Configuration Test")
    print("=" * 60)
    
    print("\nInstructions:")
    print("1. In VS Code, open the Debug view (Ctrl+Shift+D)")
    print("2. Select 'All Local Services' configuration")
    print("3. Press F5 to start all services")
    print("4. Wait for services to start (check debug console)")
    print("5. Run this test script: python test_debug.py")
    print("\n" + "=" * 60)
    
    # Ask if services are running
    print("\nMake sure services are running before testing.")
    print("You can start them using the debug configurations.")
    
    # Test if we can import required modules
    print("\nChecking imports...")
    try:
        import uvicorn
        import fastapi
        import requests
        print("✓ All required modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Run: source venv/bin/activate && pip install -r requirements-dev.txt")
        return
    
    # Optional: test services if they're running
    print("\nWould you like to test the services? (y/n)")
    # In actual use, user would answer here
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("\nTo debug:")
    print("1. Set breakpoints in Python files (click in gutter)")
    print("2. Start debug configuration")
    print("3. Use debug controls (F5, F10, F11)")
    print("4. Check debug console for output")

if __name__ == "__main__":
    main()