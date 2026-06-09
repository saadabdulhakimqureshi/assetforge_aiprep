from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from routers.auth import session_store
from routers.job_store import create_job, get_job, update_job, delete_job
from schemas.analyze import AnalyzeRequest, AnalyzeResponse
import uuid
import asyncio
import json

router = APIRouter(prefix="/api/analyze", tags=["analyze"])

@router.post("", status_code=202)
async def start_analysis(body: AnalyzeRequest, request: Request, background_tasks: BackgroundTasks):
    session_id = request.session.get("session_id")
    if not session_id or session_id not in session_store:
        return JSONResponse({"error": "unauthenticated", "message": "Not logged in", "retryable": False}, status_code=401)

    job_id = str(uuid.uuid4())
    create_job(job_id)
    background_tasks.add_task(run_pipeline, job_id, body.owner, body.repo, session_store[session_id])
    return AnalyzeResponse(job_id=job_id)

async def run_pipeline(job_id: str, owner: str, repo: str, token: str):
    try:
        update_job(job_id, status="running")

        # Step 1 — Fetch repo data
        update_job(job_id, steps=[{"step": 1, "label": "Fetching repository data...", "status": "running"}])
        await asyncio.sleep(1)  # placeholder
        update_job(job_id, steps=[{"step": 1, "label": "Fetching repository data...", "status": "complete"}])

        # Step 2 — Analyze with LLM
        update_job(job_id, steps=[{"step": 2, "label": "Analyzing repository...", "status": "running"}])
        await asyncio.sleep(1)  # placeholder
        update_job(job_id, steps=[{"step": 2, "label": "Analyzing repository...", "status": "complete"}])

        # Step 3 — Find assets
        update_job(job_id, steps=[{"step": 3, "label": "Finding matching assets...", "status": "running"}])
        await asyncio.sleep(1)  # placeholder
        update_job(job_id, steps=[{"step": 3, "label": "Finding matching assets...", "status": "complete"}])

        update_job(job_id, status="done", result={"analysis_summary": "Placeholder", "categories": {}})

    except Exception as e:
        update_job(job_id, status="error", error={"error": "pipeline_failure", "message": str(e), "retryable": True})

@router.get("/{job_id}/stream")
async def stream_analysis(job_id: str, request: Request):
    session_id = request.session.get("session_id")
    if not session_id or session_id not in session_store:
        return JSONResponse({"error": "unauthenticated", "message": "Not logged in", "retryable": False}, status_code=401)

    job = get_job(job_id)
    if not job:
        return JSONResponse({"error": "not_found", "message": "Job not found", "retryable": False}, status_code=404)

    async def event_generator():
        while True:
            job = get_job(job_id)
            if not job:
                break

            if job["status"] == "running":
                for step in job["steps"]:
                    yield f"event: progress\ndata: {json.dumps(step)}\n\n"

            elif job["status"] == "done":
                yield f"event: result\ndata: {json.dumps(job['result'])}\n\n"
                yield f"event: done\ndata: {{}}\n\n"
                delete_job(job_id)
                break

            elif job["status"] == "error":
                yield f"event: error\ndata: {json.dumps(job['error'])}\n\n"
                delete_job(job_id)
                break

            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")