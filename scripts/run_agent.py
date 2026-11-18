import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
# Force the host-local MCP URL for host-run Python processes.
os.environ["MCP_SERVER_URL"] = os.getenv("LOCAL_MCP_SERVER_URL", "http://127.0.0.1:8080/mcp")
uvicorn.run("app:app", app_dir="agent-service", host="127.0.0.1", port=8000, reload=False)
