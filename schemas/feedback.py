from pydantic import BaseModel, Field
from typing import Optional

class FeedbackRequest(BaseModel):
    job_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool