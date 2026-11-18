# Local development notes

## Most reliable first run

Use Docker Compose and `AGENT_MODE=mock`. This tests service wiring without AWS credentials or model costs.

```bash
cp .env.example .env
docker compose up --build
```

The `/agent/query` endpoint returns a deterministic message in mock mode; it intentionally does not call the MCP tools or Bedrock. Use MCP Inspector or the integration test to exercise the MCP server.

## To test real LangGraph + Bedrock locally

1. Set `AGENT_MODE=bedrock` and `BEDROCK_MODEL_ID` in `.env`.
2. Configure AWS credentials using SSO on your host.
3. For host-run Python, `AWS_PROFILE` is picked up by the AWS SDK.
4. For Docker, only pass credentials using your organization's approved local development pattern. Avoid mounting broad long-lived credentials into containers.
5. Restart the services and inspect logs.

## Direct Python run commands

The helper scripts start one process each and are intended to be run in separate terminals after installing `requirements-dev.txt` and copying `.env.example` to `.env`:

```bash
python scripts/run_rag_mock.py
python scripts/run_pipeline_mock.py
python scripts/run_mcp.py
python scripts/run_agent.py
```

If the helper scripts cannot import `uvicorn` or `dotenv`, activate the same virtual environment and run `pip install -r requirements-dev.txt`.

## Common problems

- Port conflict: change Compose host port mappings or stop the process already using 8000/8080/9000/9001.
- MCP HTTP 421: check `MCP_ALLOWED_HOSTS` against the request Host header.
- MCP connection refused: ensure mock APIs and MCP server are healthy before starting agent.
- Bedrock access denied: check selected AWS profile/task role, model ID, Region, account model access, and inference profile permissions.
- `rag-mock` hostname fails from host shell: use `127.0.0.1`; Compose service DNS names only work inside the Compose network.
- Existing API response mismatch: update `mcp-server/app.py` request/response mapping to match the real API.
