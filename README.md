# RAG Agent Platform: LangGraph + Amazon Bedrock + MCP

A local-first starter project that exposes an existing RAG API and an operational API through a private MCP server, then calls those tools from a LangGraph agent using Amazon Bedrock.

This is a starter implementation, not a turnkey production deployment. Review all configuration, dependency versions, API contracts, and authorization rules before using it with real data.

## Architecture

- `mcp-server`: MCP Streamable HTTP server with `search_knowledge_base` and `get_pipeline_status`.
- `agent-service`: FastAPI service running a LangGraph ReAct agent, LangChain MCP adapters, and Amazon Bedrock Converse.
- `mock-backends`: optional local RAG and pipeline APIs so the complete flow works before connecting your existing services.
- `ecs/`: task definition templates and sample IAM policy/trust policy.
- `tests/`: unit and local integration tests.
- Docker Compose runs the full stack locally.

## Prerequisites

- Python 3.11+ (Python 3.12 recommended)
- Docker Desktop / Docker Engine with Docker Compose v2
- AWS CLI v2 only if you want to test with Amazon Bedrock
- An AWS profile/SSO session authorized to invoke your selected Bedrock model
- Access to a Bedrock model in the chosen AWS Region

## Quick start: run everything locally with mock services

This mode does not call AWS or require AWS credentials.

1. Copy local environment settings:

   ```bash
   cp .env.example .env
   ```

2. Start the complete stack:

   ```bash
   docker compose up --build
   ```

3. Check health:

   ```bash
   curl http://localhost:8000/health
   curl http://localhost:9000/health
   curl http://localhost:9001/health
   ```

4. Ask a question through the agent API:

   ```bash
   curl -sS -X POST http://localhost:8000/agent/query \
     -H 'Content-Type: application/json' \
     -d '{"question":"What is our document ingestion process?"}'
   ```

   The mock backends return sample information, but the agent still uses Bedrock. To run fully without Bedrock, see **Mock LLM mode** below.

5. Test MCP tool discovery with the official MCP Inspector if desired:

   ```bash
   npx -y @modelcontextprotocol/inspector
   ```

   Connect it to `http://localhost:8080/mcp`.

## Mock LLM mode (no AWS required)

For a fully offline wiring test, set `AGENT_MODE=mock` in `.env`. In this mode, `/agent/query` returns a deterministic response and does not invoke LangGraph or Bedrock. The MCP server and mock APIs still run and can be tested independently. This mode is for local plumbing only, not for evaluating agent behavior.

Restart after changing `.env`:

```bash
docker compose up --build
```

## Local Python development (without Docker)

Create separate virtual environments or use the root development requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

Run mock backend services in separate terminals:

```bash
uvicorn mock-backends.rag_api:app --host 127.0.0.1 --port 9000
uvicorn mock-backends.pipeline_api:app --host 127.0.0.1 --port 9001
```

Python package names cannot contain hyphens in import paths; for direct `uvicorn` commands, use the provided helper commands below instead:

```bash
python scripts/run_rag_mock.py
python scripts/run_pipeline_mock.py
```

Run the MCP server in another terminal:

```bash
python scripts/run_mcp.py
```

Run the agent API in another terminal:

```bash
python scripts/run_agent.py
```

When running Python processes directly on your host, use these URLs in `.env`:

```dotenv
RAG_API_URL=http://127.0.0.1:9000
PIPELINE_API_URL=http://127.0.0.1:9001
MCP_SERVER_URL=http://127.0.0.1:8080/mcp
```

Note: `scripts/run_mcp.py` and `scripts/run_agent.py` load `.env` via `python-dotenv` and set local defaults. Docker Compose uses service names such as `rag-mock` and `mcp-server`; those names do not resolve from your host shell.

## Run with Amazon Bedrock locally

1. Configure AWS credentials using your organization's approved method, preferably IAM Identity Center / AWS SSO:

   ```bash
   aws configure sso
   aws sso login --profile YOUR_PROFILE
   export AWS_PROFILE=YOUR_PROFILE
   export AWS_REGION=us-east-1
   ```

2. Verify the identity:

   ```bash
   aws sts get-caller-identity --profile YOUR_PROFILE
   ```

3. In `.env`, set:

   ```dotenv
   AGENT_MODE=bedrock
   AWS_REGION=us-east-1
   BEDROCK_MODEL_ID=YOUR_APPROVED_BEDROCK_MODEL_ID
   ```

4. For **host-run Python**, boto3/botocore uses the selected profile. For Docker, credentials are not automatically shared safely by default. For local Docker testing, use an approved credential setup and mount/configure AWS credentials only if your security policy permits it. Never bake credentials into an image or commit them to `.env`.

5. Invoke the API. Bedrock access, model availability, quotas, and possible model access setup depend on your AWS account and Region.

## Connect to your existing APIs

Replace the mock backend URLs with your reachable existing API URLs.

- `RAG_API_URL`: base URL for your RAG API. Expected example contract: `POST /query` with `{"question":"..."}`.
- `PIPELINE_API_URL`: base URL for the operational API. Expected example contract: `GET /executions/{execution_id}`.

Adapt `mcp-server/app.py` to your actual request/response contracts, authentication, and authorization. Do not expose arbitrary SQL or unrestricted internal APIs as tools.

## API contract

Request:

```json
{"question":"What is our document ingestion process?"}
```

Response shape:

```json
{
  "answer":"...",
  "tools_used":["search_knowledge_base"]
}
```

`tools_used` indicates tool calls attempted by the model, not necessarily successful tool execution.

## Tests

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
pytest -q
```

Run integration tests that use local mock APIs and MCP server:

```bash
RUN_INTEGRATION=1 pytest -q
```

The integration test uses `AGENT_MODE=mock` for a no-AWS test. It verifies MCP discovery and the MCP tool call path separately from model reasoning.

## Docker Compose services

- Agent API: http://localhost:8000
- MCP endpoint: http://localhost:8080/mcp
- Mock RAG API: http://localhost:9000
- Mock pipeline API: http://localhost:9001

The MCP endpoint is exposed on localhost only in Compose. Do not expose it publicly without authentication and an explicit authorization design.

## AWS deployment notes

The `ecs/` files are templates. Before deploying:
- Replace account IDs, image URIs, model IDs, role ARNs, subnet IDs, security groups, and namespace values.
- Create ECR repositories and CloudWatch log groups.
- Create ECS task execution and task roles separately.
- Ensure service-connect port names match task-definition port mapping names.
- Ensure the MCP SDK Host allowlist matches the actual `Host` header.
- Add the authentication mechanism required by your organization for agent-to-MCP calls.
- Configure network egress or VPC endpoints for ECR, CloudWatch Logs, Secrets Manager if used, and Bedrock Runtime.
- Review the Bedrock IAM resource ARN for your chosen model/inference profile.
- Validate task-definition JSON and IAM policies before production use.
