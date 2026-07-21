"""
OpenForge AI - Integrated Application Launcher
Starts FastAPI backend server on port 8000 and Vite frontend on port 5173.
"""

import os
import sys
import subprocess
import time
import socket
import webbrowser

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def kill_port_8000_windows():
    """Frees port 8000 if occupied by a stale process on Windows."""
    if os.name == "nt":
        try:
            cmd = "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            time.sleep(1)
        except Exception:
            pass

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def main():
    print("==================================================")
    print("      🚀 Launching OpenForge AI Platform          ")
    print("==================================================")

    # Free port 8000 if in use
    if is_port_in_use(8000):
        print("-> Cleaning up stale process on port 8000...")
        kill_port_8000_windows()

    print("-> Backend:  http://127.0.0.1:8000")
    print("-> Frontend: http://localhost:5173")
    print("--------------------------------------------------")

    # Start FastAPI Backend
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=BACKEND_DIR
    )

    # Start Vite Frontend
    npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
    frontend_proc = subprocess.Popen(
        [npx_cmd, "vite", "--port", "5173"],
        cwd=FRONTEND_DIR
    )

    print("\nPress Ctrl+C to stop both servers.\n")
    time.sleep(3)

    try:
        webbrowser.open("http://localhost:5173")
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down OpenForge AI servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
