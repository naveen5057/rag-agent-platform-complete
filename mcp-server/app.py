import os
import re
import logging

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("rag-mcp")

RAG_API_URL = os.environ["RAG_API_URL"].rstrip("/")
PIPELINE_API_URL = os.environ["PIPELINE_API_URL"].rstrip("/")
TIMEOUT = httpx.Timeout(30.0, connect=3.0)
from mcp.server.transport_security import TransportSecuritySettings
security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "mcp-server",
        "mcp-server:8080",
        "mcp-server:*",
        "localhost",
        "localhost:8080",
    ],
)

mcp = FastMCP(

    "rag-platform-tools",
    instructions=(
        "Read-only tools for searching the internal knowledge base "
        "and retrieving pipeline execution status."
    ),
    stateless_http=True,
    json_response=True,
    transport_security=security,
)


@mcp.tool()
async def search_knowledge_base(question: str) -> dict:
    """Search the internal knowledge base and return an answer and sources."""
    question = question.strip()
    if not question or len(question) > 4000:
        raise ValueError("question must contain 1-4000 characters")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(
            f"{RAG_API_URL}/query",
            json={"question": question},
        )
        response.raise_for_status()
        result = response.json()

    if not isinstance(result, dict):
        raise ValueError("RAG API returned an unexpected response")
    return result


@mcp.tool()
async def get_pipeline_status(execution_id: str) -> dict:
    """Get the status of one pipeline execution."""
    execution_id = execution_id.strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", execution_id):
        raise ValueError("Invalid execution ID")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(
            f"{PIPELINE_API_URL}/executions/{execution_id}"
        )
        response.raise_for_status()
        result = response.json()

    if not isinstance(result, dict):
        raise ValueError("Pipeline API returned an unexpected response")
    return result


# Create MCP app with explicit path
app = mcp.streamable_http_app()

# Try to add a simple health endpoint
# Note: This might not work if the MCP app doesn't support adding routes
try:
    # Try to monkey-patch a health endpoint
    # This is a hack, but might work
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    
    async def health(request):
        return JSONResponse({"status": "ok", "service": "mcp-server"})
    
    # Try to add route to app.routes
    if hasattr(app, 'routes'):
        app.routes.append(Route("/health", health, methods=["GET"]))
        logger.info("Added health endpoint to MCP app")
    else:
        logger.warning("Cannot add health endpoint - app has no routes attribute")
except Exception as e:
    logger.warning(f"Could not add health endpoint: {e}")
    # Continue without health endpoint - docker healthcheck uses TCP anyway