from sqlmodel import SQLModel, Field
from typing import Optional


class Asset(SQLModel, table=True):
    __tablename__ = "assets"

    id: str = Field(primary_key=True)
    name: str
    category: str
    source: str
    license: str
    url: str
    thumbnail_url: Optional[str] = None
    tags: Optional[str] = None       # JSON array stored as string
    description: Optional[str] = None


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: str = Field(primary_key=True)
    user_login: str
    repo_owner: str
    repo_name: str
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: str
