import subprocess
import sys
import time
import os

def run_fastapi():
    """Run FastAPI server"""
    print("🚀 Starting FastAPI server...")
    subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ], cwd=project_dir)  # Chỉ định thư mục làm việc

def run_streamlit():
    """Run Streamlit app"""
    print("🎨 Starting Streamlit app...")
    time.sleep(3)  # Wait for FastAPI to start
    subprocess.Popen([
        sys.executable, "-m", "streamlit",
        "run", "src/streamlit_app.py"
    ], cwd=project_dir)  # Chỉ định thư mục làm việc

if __name__ == "__main__":
    print("=" * 60)
    print("💰 Finance AI Agent - Starting Services")
    print("=" * 60)
    
    # Get the project directory automatically
    current_file = os.path.abspath(__file__) 
    project_dir = os.path.dirname(os.path.dirname(current_file))  
    
    print(f"📁 Project directory: {project_dir}\n")
    
    # Start FastAPI
    run_fastapi()
    
    # Start Streamlit
    run_streamlit()
    
    print("\n✅ Services started!")
    print("📊 FastAPI API: http://localhost:8000")
    print("🎨 Streamlit UI: http://localhost:8501")
    print("\nPress Ctrl+C to stop all services")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        sys.exit(0)