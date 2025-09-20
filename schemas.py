from pydantic import BaseModel

class RepoRequest(BaseModel):
    repo_url: str = None  # If provided, clone this repo
    local_path: str = None  # If provided, use this local path
