from repositories.base import ReadWriteRepo
from repositories.models import Session
from datetime import datetime, timezone


class SessionsRepo(ReadWriteRepo):
    async def create_session(self, id: str, user_login: str, repo_owner: str, repo_name: str) -> Session:
        return await self.create(Session(
            id=id,
            user_login=user_login,
            repo_owner=repo_owner,
            repo_name=repo_name,
            created_at=datetime.now(timezone.utc).isoformat()
        ))

    async def update_feedback(self, id: str, rating: int, comment: str | None) -> Session | None:
        session = await self.get_one(Session, id=id)
        if session:
            session.rating = rating
            session.comment = comment
            return await self.update(session)
        return None

    async def get_by_id(self, id: str) -> Session | None:
        return await self.get_one(Session, id=id)
