from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from routers.auth import session_store
from services.session_logger import save_feedback
from schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.post("")
async def submit_feedback(body: FeedbackRequest, request: Request):
    session_id = request.session.get("session_id")
    if not session_id or session_id not in session_store:
        return JSONResponse({"error": "unauthenticated", "message": "Not logged in", "retryable": False}, status_code=401)
    
    result = await save_feedback(body.job_id, body.rating, body.comment)
    if result is None:
        return JSONResponse({"error": "not_found", "message": "Job not found", "retryable": False}, status_code=404)
    
    return FeedbackResponse(success=True)