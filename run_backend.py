import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure current directory is in PYTHONPATH
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    is_dev = os.environ.get("ENVIRONMENT", "development").lower() != "production"
    
    print(f"🛡️ Starting CyberNewsAI on http://{host}:{port} (Dev reload: {is_dev}) ...")
    uvicorn.run("backend.main:app", host=host, port=port, reload=is_dev)
