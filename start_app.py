# start_app.py
"""
Python starter script to activate venv and run FastAPI app with Uvicorn.
"""
import os
import sys
import subprocess

venv_path = os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")

if not os.path.exists(venv_path):
    print("Virtual environment not found. Please create one and install requirements.")
    sys.exit(1)

# Use venv's python to run uvicorn
try:
    subprocess.check_call([
        venv_path, "-m", "uvicorn", "main:app", "--reload"
    ])
except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error starting app: {e}")
    sys.exit(1)
