# VS Code Debug Configuration Setup

This guide explains how to set up and use the debug configurations for the RAG Agent Platform.

## Prerequisites

1. Python 3.10 or higher
2. VS Code with Python extension installed
3. Virtual environment setup (see below)

## Quick Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

Or in VS Code:
1. Press `Ctrl+Shift+P` (Cmd+Shift+P on macOS)
2. Type "Run Task"
3. Select "Setup Development Environment"

## Debug Configurations

The following debug configurations are available in `.vscode/launch.json`:

### Individual Services
- **Agent Service (FastAPI)** - Port 8000
- **MCP Server** - Port 8080  
- **Mock RAG API** - Port 9000
- **Mock Pipeline API** - Port 9001

### Compound Configurations (run multiple services)
- **All Local Services** - All 4 services together
- **Full Stack** - Mock backends + MCP + Agent
- **Backend Services Only** - Mock APIs + MCP

### Other Configurations
- **Python: Current File** - Debug the currently open Python file
- **Python: Run Script** - Run scripts from the scripts/ directory
- **Docker Compose: All Services** - Run via Docker Compose
- **Python: Attach** - Attach to an existing Python process

## How to Use

1. **Open the Debug View**:
   - Click the bug icon in the activity bar
   - Or press `Ctrl+Shift+D` (Cmd+Shift+D on macOS)

2. **Select a Configuration** from the dropdown

3. **Start Debugging**:
   - Press `F5` to start debugging
   - Or click the green play button

4. **Set Breakpoints**:
   - Click in the gutter next to line numbers
   - Red dots indicate breakpoints

5. **Debug Controls**:
   - Continue (F5) - Resume execution
   - Step Over (F10) - Step over current line
   - Step Into (F11) - Step into function calls
   - Step Out (Shift+F11) - Step out of current function
   - Restart (Ctrl+Shift+F5) - Restart debugging
   - Stop (Shift+F5) - Stop debugging

## Environment Variables

Debug configurations include environment variables for local development:

- `AGENT_MODE=mock` - Use mock mode (no Bedrock calls)
- `LOG_LEVEL=DEBUG` - Enable debug logging
- Service URLs configured for localhost

## Common Issues

### "No module named uvicorn"
Solution: Run the setup script to install dependencies:
```bash
./setup.sh
```

### Debugger doesn't stop at breakpoints
Solution: Ensure `justMyCode: false` is set in launch.json (already configured)

### Port conflicts
Solution: Check if services are already running on the required ports:
```bash
lsof -i :8000  # Check port 8000
lsof -i :8080  # Check port 8080
lsof -i :9000  # Check port 9000
lsof -i :9001  # Check port 9001
```

## Testing

Run tests with:
```bash
pytest
```

Or use the "Run Tests" task in VS Code.

## Tips

1. Use the **compound configurations** to debug multiple services together
2. The `--reload` flag enables hot reloading when code changes
3. Check the debug console for service logs and output
4. Use environment variables in `.env` for configuration

## File Structure

```
.vscode/
├── launch.json    # Debug configurations
├── tasks.json     # Build and run tasks
└── settings.json  # VS Code settings
```

## Support

If you encounter issues:
1. Run the environment check: `python check_environment.py`
2. Verify virtual environment: `which python` should point to `venv/bin/python`
3. Reinstall dependencies: `pip install -r requirements-dev.txt`