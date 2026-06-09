from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from integrations.github_client import exchange_code, get_user_info
import os
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

# In-memory store: { session_id: github_token }
session_store:dict[str, str] = {}


# Redirects the user to GitHub's OAuth page:
@router.get("/github")
def github_login():
    client_id = os.getenv("GITHUB_CLIENT_ID")
    scope = "read:user repo"
    redirect_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}"
    return RedirectResponse(redirect_url)

# GitHub calls this after the user approves. Exchange the code, store the token, set the session cookie.
@router.get("/callback")
async def github_callback(code: str, request: Request):
    token = await exchange_code(code)
    if not token:
        return JSONResponse({"error": "oauth_failed", "message": "GitHub OAuth failed", "retryable": False}, status_code=400)
    
    session_id = str(uuid.uuid4())
    session_store[session_id] = token
    request.session["session_id"] = session_id

    frontend_url = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    return RedirectResponse(f"{frontend_url}/repos")

@router.get("/me")
async def get_me(request: Request):
    session_id = request.session.get("session_id")
    if not session_id or session_id not in session_store:
        return JSONResponse({"error": "unauthenticated", "message": "Not logged in", "retryable": False}, status_code=401)
    
    token = session_store[session_id]
    user = await get_user_info(token)
    return {"login": user["login"], "avatar_url": user["avatar_url"], "name": user.get("name")}


@router.get("/logout")
def logout(request: Request):
    session_id = request.session.get("session_id")
    if session_id in session_store:
        del session_store[session_id]
    request.session.clear()
    return {"success": True}