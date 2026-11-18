#!/usr/bin/env python3
"""Check if the development environment is properly set up."""

import sys
import subprocess

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 10:
        print("  ✓ Python version is compatible (3.10+)")
        return True
    else:
        print("  ✗ Python 3.10 or higher is required")
        return False

def check_module(module_name):
    """Check if a Python module is installed."""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"  ✗ {module_name} is NOT installed")
        return False

def check_required_modules():
    """Check all required modules."""
    print("\nChecking required modules...")
    modules = [
        "uvicorn",
        "fastapi",
        "httpx",
        "pydantic",
        "boto3",
        "pytest"
    ]
    
    results = [check_module(m) for m in modules]
    return all(results)

def main():
    print("=" * 60)
    print("RAG Agent Platform - Environment Check")
    print("=" * 60)
    
    python_ok = check_python_version()
    modules_ok = check_required_modules()
    
    print("\n" + "=" * 60)
    
    if python_ok and modules_ok:
        print("✓ Environment is properly set up!")
        print("\nYou can now run debug configurations in VS Code:")
        print("1. Press F5 to start debugging")
        print("2. Select 'All Local Services' to run the full stack")
        print("3. Set breakpoints in any Python file")
        return 0
    else:
        print("✗ Environment setup incomplete")
        print("\nTo set up the environment:")
        print("1. Run: ./setup.sh")
        print("2. Or in VS Code: Run Task -> Setup Development Environment")
        return 1

if __name__ == "__main__":
    sys.exit(main())