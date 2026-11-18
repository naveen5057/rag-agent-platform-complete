from fastapi import FastAPI, HTTPException
import re

app = FastAPI(title="Local Mock Pipeline API")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "pipeline-mock"}


@app.get("/executions/{execution_id}")
async def execution_status(execution_id: str):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", execution_id):
        raise HTTPException(status_code=400, detail="Invalid execution ID")

    return {
        "execution_id": execution_id,
        "status": "FAILED" if execution_id.lower().startswith("fail") else "SUCCEEDED",
        "error_category": (
            "SOURCE_TIMEOUT" if execution_id.lower().startswith("fail") else None
        ),
        "message": (
            "Sample failure: source request timed out."
            if execution_id.lower().startswith("fail")
            else "Mock execution completed successfully."
        ),
        "mock": True,
    }
