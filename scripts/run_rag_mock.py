import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()
uvicorn.run("rag_api:app", app_dir="mock-backends", host="127.0.0.1", port=9000, reload=False)
