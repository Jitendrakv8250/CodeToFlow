
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi import HTTPException
import os
import shutil
import subprocess
from schemas import RepoRequest
from pydantic import BaseModel
from langgraph_ollama import analyze_codebase_with_ollama
from mermaid_render import render_mermaid_to_image
# Endpoint to analyze codebase and generate UML
from fastapi import BackgroundTasks

app = FastAPI()
# Endpoint to get UML image

@app.get("/uml/{project_name}")
def get_uml_image(project_name: str):
    site_dir = os.path.join(os.getcwd(), "site", project_name)
    image_path = os.path.join(site_dir, "uml.svg")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="UML image not found. Analysis may still be running.")
    return FileResponse(image_path, media_type="image/svg+xml")

# Endpoint to get Mermaid code
@app.get("/uml/{project_name}/mermaid")
def get_uml_mermaid(project_name: str):
    site_dir = os.path.join(os.getcwd(), "site", project_name)
    mmd_path = os.path.join(site_dir, "uml.mmd")
    if not os.path.exists(mmd_path):
        raise HTTPException(status_code=404, detail="Mermaid code not found. Analysis may still be running.")
    with open(mmd_path, encoding="utf-8") as f:
        return JSONResponse({"mermaid": f.read()})






class AnalyzeRequest(BaseModel):
    project_name: str

@app.post("/analyze")
def analyze_repo(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    codebase_path = os.path.join(os.getcwd(), req.project_name)
    if not os.path.exists(codebase_path):
        raise HTTPException(status_code=404, detail="Project not found")
    # Run analysis (can be slow, so use background task)
    def do_analysis():
        mermaid_code = analyze_codebase_with_ollama(codebase_path)
        if not mermaid_code.strip():
            return
        site_dir = os.path.join(os.getcwd(), "site", req.project_name)
        os.makedirs(site_dir, exist_ok=True)
        image_path = os.path.join(site_dir, "uml.svg")
        render_mermaid_to_image(mermaid_code, image_path)
        # Also save the Mermaid code for reference
        with open(os.path.join(site_dir, "uml.mmd"), "w", encoding="utf-8") as f:
            f.write(mermaid_code)
    background_tasks.add_task(do_analysis)
    return {"message": "Analysis started. Check site/{req.project_name}/uml.svg when done."}

@app.get("/")
def root():
    return {"message": "AI UML Agent is running."}



# Endpoint to clone a GitHub repo
class RepoCloneRequest(BaseModel):
    repo_url: str

@app.post("/repo/clone")
def clone_repo(req: RepoCloneRequest):
    project_name = req.repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    dest_path = os.path.join(os.getcwd(), project_name)
    if os.path.exists(dest_path):
        return {"message": f"Repo already exists at {dest_path}", "project_name": project_name}
    try:
        subprocess.check_call(["git", "clone", req.repo_url, dest_path])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Git clone failed: {e}")
    return {"message": "Repo cloned", "project_name": project_name}

# Endpoint to use a local repo path
class RepoLocalRequest(BaseModel):
    local_path: str

@app.post("/repo/local")
def use_local_repo(req: RepoLocalRequest):
    if not os.path.exists(req.local_path):
        raise HTTPException(status_code=404, detail="Local path does not exist")
    project_name = os.path.basename(os.path.normpath(req.local_path))
    dest_path = os.path.join(os.getcwd(), project_name)
    if os.path.exists(dest_path):
        return {"message": f"Repo already exists at {dest_path}", "project_name": project_name}
    try:
        shutil.copytree(req.local_path, dest_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copy failed: {e}")
    return {"message": "Local repo copied", "project_name": project_name}
