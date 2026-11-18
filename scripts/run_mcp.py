import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
# Force host-local URLs for host-run Python processes; Compose uses service DNS.
os.environ["RAG_API_URL"] = os.getenv("LOCAL_RAG_API_URL", "http://127.0.0.1:9000")
os.environ["PIPELINE_API_URL"] = os.getenv("LOCAL_PIPELINE_API_URL", "http://127.0.0.1:9001")
os.environ["MCP_ALLOWED_HOSTS"] = "localhost:8080,127.0.0.1:8080"
uvicorn.run("app:app", app_dir="mcp-server", host="127.0.0.1", port=8080, reload=False)
