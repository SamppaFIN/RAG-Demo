#!/usr/bin/env python3
"""
AI Candy Store RAG Demo - Startup Script
Starts both backend and frontend servers simultaneously
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def print_banner():
    banner = """
    🍭 AI Candy Store RAG Demo 🍭
    ================================
    Starting interactive RAG demonstration...
    
    Backend:  http://localhost:8000
    Frontend: http://localhost:3000
    
    Press Ctrl+C to stop both servers
    ================================
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are available"""
    # Check Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if backend dependencies exist
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return False
    
    # Check if frontend dependencies exist
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🔧 Starting backend server...")
    backend_path = Path("backend")
    
    # Change to backend directory and start server
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_path.absolute())
    
    return subprocess.Popen(
        [sys.executable, "openai_main.py"],
        cwd=backend_path,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

def start_frontend():
    """Start the React frontend server"""
    print("🎨 Starting frontend server...")
    frontend_path = Path("frontend")
    
    # Check if node_modules exists
    if not (frontend_path / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        install_process = subprocess.run(
            ["npm", "install"],
            cwd=frontend_path,
            capture_output=True,
            text=True
        )
        
        if install_process.returncode != 0:
            print("❌ Failed to install frontend dependencies")
            print(install_process.stderr)
            return None
    
    return subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

def install_backend_deps():
    """Install backend dependencies if needed"""
    backend_path = Path("backend")
    requirements_file = backend_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found in backend directory")
        return False
    
    print("📦 Installing backend dependencies...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=backend_path,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Backend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        print(e.stderr)
        return False

def main():
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    # Install backend dependencies
    if not install_backend_deps():
        sys.exit(1)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            print("❌ Failed to start backend")
            sys.exit(1)
        
        # Wait a moment for backend to start
        print("⏳ Waiting for backend to initialize...")
        time.sleep(3)
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Failed to start frontend")
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
        
        print("✅ Both servers are starting up!")
        print("🌐 Frontend will be available at: http://localhost:3000")
        print("🔧 Backend API available at: http://localhost:8000")
        print("📖 API docs available at: http://localhost:8000/docs")
        print("\n⏰ Please wait a moment for both servers to fully initialize...")
        print("🛑 Press Ctrl+C to stop both servers\n")
        
        # Monitor both processes
        while True:
            # Check if processes are still running
            backend_running = backend_process.poll() is None
            frontend_running = frontend_process.poll() is None
            
            if not backend_running:
                print("❌ Backend process stopped unexpectedly")
                break
            
            if not frontend_running:
                print("❌ Frontend process stopped unexpectedly")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
    
    finally:
        # Clean up processes
        if backend_process:
            print("🔧 Stopping backend...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process:
            print("🎨 Stopping frontend...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("✅ Servers stopped. Thank you for using AI Candy Store RAG Demo! 🍭")

if __name__ == "__main__":
    main() 