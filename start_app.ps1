# start_app.ps1
# PowerShell script to activate venv and start FastAPI app with Uvicorn

$venvPath = "./venv/Scripts/Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    . $venvPath
} else {
    Write-Host "Virtual environment not found. Please create one and install requirements."
    exit 1
}

Write-Host "Starting FastAPI app with Uvicorn..."
uvicorn main:app --reload
