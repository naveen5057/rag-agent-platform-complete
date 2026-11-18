#!/bin/bash

echo "Setting up RAG Agent Platform development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements-dev.txt..."
pip install -r requirements-dev.txt

# Verify installation
echo "Verifying installation..."
python -c "import uvicorn; import fastapi; print('Dependencies installed successfully!')"

echo ""
echo "Setup complete! To activate the virtual environment, run:"
echo "source venv/bin/activate"
echo ""
echo "Then you can run the debug configurations in VS Code."