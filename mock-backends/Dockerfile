FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN pip install --no-cache-dir fastapi 'uvicorn[standard]'
COPY mock-backends/rag_api.py /app/rag_api.py
COPY mock-backends/pipeline_api.py /app/pipeline_api.py
