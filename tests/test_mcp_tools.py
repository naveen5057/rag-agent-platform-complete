import os
import pytest
import httpx

BASE = os.getenv("MCP_TEST_BASE_URL", "http://127.0.0.1:8080")


@pytest.mark.asyncio
async def test_mock_backends_health():
    async with httpx.AsyncClient() as client:
        rag = await client.get("http://127.0.0.1:9000/health")
        pipeline = await client.get("http://127.0.0.1:9001/health")
    assert rag.status_code == 200
    assert pipeline.status_code == 200


@pytest.mark.asyncio
@pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="set RUN_INTEGRATION=1")
async def test_mcp_endpoint_accepts_initialize():
    # Minimal MCP Streamable HTTP initialize request.
    # MCP protocol versions can change; use MCP Inspector for authoritative tests.
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "local-test", "version": "0.1.0"}
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE}/mcp",
            json=payload,
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "MCP-Protocol-Version": "2025-03-26",
            },
        )
    assert response.status_code in (200, 202)
