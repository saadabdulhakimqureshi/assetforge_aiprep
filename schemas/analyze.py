from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    owner: str
    repo: str

class AnalyzeResponse(BaseModel):
    job_id: str