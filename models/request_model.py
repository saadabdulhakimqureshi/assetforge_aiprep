from pydantic import BaseModel

class ProjectContext(BaseModel):
    description: str
    genres: list[str] = []
    setting: str | None = None