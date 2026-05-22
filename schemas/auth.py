from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    login: str
    avatar_url: str
    name: Optional[str] = None