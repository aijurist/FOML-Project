import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Starts a Uvicorn server.

    Args:
        host(str): The host address to bind to. Defaults to "0.0.0.0" (all interfaces).
        port(int): The port number to listen on. Defaults to 8000.
        reload(bool): Whether to enable auto-reload on code changes. Defaults to True.

    Returns:
        None: This function does not return a value.

    Raises:
        Exception: Any exception raised during server startup.
    """
    print(f"Starting server on {host}:{port}")
    
    uvicorn.run("api.app:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    start_server()