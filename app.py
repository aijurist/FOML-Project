import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI server with the given configuration"""
    print(f"Starting server on {host}:{port}")
    
    uvicorn.run("api.app:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    start_server()