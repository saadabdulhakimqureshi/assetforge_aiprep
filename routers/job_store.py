from typing import Any

jobs: dict[str, dict[str, Any]] = {}

def create_job(job_id: str):
    jobs[job_id] = {
        "status": "pending",
        "steps": [],
        "result": None,
        "error": None,
    }

def get_job(job_id: str):
    return jobs.get(job_id)

def delete_job(job_id: str):
    jobs.pop(job_id, None)

def update_job(job_id: str, **kwargs):
    if job_id in jobs:
        jobs[job_id].update(kwargs)