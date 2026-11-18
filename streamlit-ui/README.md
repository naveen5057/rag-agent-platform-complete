# Streamlit UI for RAG Agent Platform

A user-friendly web interface to interact with your RAG Agent Platform.

## Features

- **Chat Interface**: Ask questions to the AI agent in a conversational format
- **Conversation History**: View past questions and answers
- **Tool Usage Tracking**: See which MCP tools were used for each response
- **Service Status Monitoring**: Real-time status of backend services
- **Response Details**: Detailed view of agent responses
- **Example Questions**: Quick access to common queries

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Streamlit UI   │────▶│  Agent Service  │────▶│   MCP Server    │
│   (Port 8501)   │     │   (Port 8000)   │     │   (Port 8080)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                     ┌─────────────────┐     ┌─────────────────┐
                     │  Mock RAG API   │     │ Mock Pipeline   │
                     │   (Port 9000)   │     │   (Port 9001)   │
                     └─────────────────┘     └─────────────────┘
```

## Installation

The Streamlit UI is already included in the project dependencies. To install:

```bash
# From project root
./setup.sh

# Or manually
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Running the UI

### Option 1: VS Code Debug Configuration (Recommended)

1. Open the Debug view (Ctrl+Shift+D or Cmd+Shift+D)
2. Select **"Complete Platform with UI"** to run everything
3. Or select **"Streamlit UI"** to run just the UI (requires backend services)
4. Press F5 to start

### Option 2: Command Line

```bash
# Start backend services first (in separate terminals)
uvicorn agent-service.app:app --host 0.0.0.0 --port 8000 --reload
uvicorn mcp-server.app:app --host 0.0.0.0 --port 8080 --reload
uvicorn mock-backends.rag_api:app --host 0.0.0.0 --port 9000 --reload
uvicorn mock-backends.pipeline_api:app --host 0.0.0.0 --port 9001 --reload

# Then start Streamlit UI
streamlit run streamlit-ui/app.py
```

### Option 3: Docker Compose

```bash
docker-compose up
# The Streamlit UI will be available at http://localhost:8501
```

## Usage

1. **Open the UI**: Navigate to http://localhost:8501
2. **Check Service Status**: The sidebar shows if backend services are running
3. **Ask Questions**: Type your question in the input field and press Submit
4. **View Responses**: See answers in the conversation history with tool usage
5. **Clear Conversation**: Use the sidebar button to start fresh

## UI Components

### Sidebar
- Service status indicators
- Clear conversation button
- Debug information
- About section

### Main Area
- **Chat Interface**: Input field and submit button
- **Conversation History**: Scrollable chat history with timestamps
- **Response Details**: Detailed view of the last response
- **Quick Actions**: Example questions and service checks

## Configuration

The UI can be configured via environment variables:

```bash
# In .env file or environment
AGENT_SERVICE_URL=http://localhost:8000
MCP_SERVER_URL=http://localhost:8080
```

## Testing

Run the integration test:

```bash
python streamlit-ui/test_integration.py
```

## Development

### Adding New Features

1. **New UI Components**: Add to `streamlit-ui/app.py`
2. **Environment Variables**: Update configuration in the app
3. **Dependencies**: Add to `streamlit-ui/requirements.txt`

### Debugging

1. Use VS Code debug configurations
2. Check Streamlit logs in the terminal
3. Verify backend service connections
4. Test with the integration script

## Troubleshooting

### Common Issues

1. **"Cannot connect to agent service"**
   - Ensure Agent Service is running on port 8000
   - Check `AGENT_SERVICE_URL` environment variable

2. **"Streamlit not found"**
   - Install dependencies: `pip install -r requirements-dev.txt`
   - Activate virtual environment: `source venv/bin/activate`

3. **Port conflicts**
   - Check if ports 8501, 8000, 8080, 9000, 9001 are in use
   - Change ports in configuration if needed

4. **Slow responses**
   - Check agent service logs
   - Verify MCP server connections
   - Increase timeout in UI configuration

### Logs

- Streamlit logs appear in the terminal
- Backend service logs are in their respective terminals
- Debug information available in UI sidebar

## Example Questions

Try these example questions:

1. "What is the ingestion process for documents?"
2. "Check the status of pipeline execution ABC123"
3. "How does the RAG system work?"
4. "What tools are available in the MCP server?"

## Contributing

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Test integration with all services

## License

Part of the RAG Agent Platform project.