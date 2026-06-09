from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from integrations.github_client import get_user_repos
from routers.auth import session_store

router = APIRouter(prefix="/api/repos", tags=["repos"])

@router.get("")
async def list_repos(request: Request):
    session_id = request.session.get("session_id")
    if not session_id or session_id not in session_store:
        return JSONResponse({"error": "unauthenticated", "message": "Not logged in", "retryable": False}, status_code=401)
    
    token = session_store[session_id]
    repos = await get_user_repos(token)

    return [
        {
            "owner": repo["owner"]["login"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo.get("description"),
            "private": repo["private"],
            "updated_at": repo["updated_at"],
        }
        for repo in repos
        if not repo.get("fork")  # exclude forks
    ]