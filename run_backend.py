import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure current directory is in PYTHONPATH
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    print("🛡️ Starting CyberNewsAI FastAPI Threat Intelligence Server on http://localhost:8000 ...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
