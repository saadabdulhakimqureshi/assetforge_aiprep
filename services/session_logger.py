from repositories.sessions_repo import SessionsRepo

repo = SessionsRepo()

async def create_session(job_id: str, user_login: str, repo_owner: str, repo_name: str):
    await repo.create_session(
        id=job_id,
        user_login=user_login,
        repo_owner=repo_owner,
        repo_name=repo_name
    )

async def save_feedback(job_id: str, rating: int, comment: str | None):
    session = await repo.get_by_id(job_id)
    if not session:
        return None
    return await repo.update_feedback(job_id, rating, comment)