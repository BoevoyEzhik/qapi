from fastapi import Depends

from app.db.database import get_async_session
from app.repositories.answer_repository import AnswerRepository
from app.repositories.question_repository import QuestionRepository
from app.services.answer_service import AnswerService
from app.services.question_service import QuestionService


async def get_question_repository(
    session=Depends(get_async_session),
) -> QuestionRepository:
    return QuestionRepository(session)


async def get_question_service(
    user_repo=Depends(get_question_repository),
) -> QuestionService:
    return QuestionService(user_repo)


async def get_answer_repository(session=Depends(get_async_session)) -> AnswerRepository:
    return AnswerRepository(session)


async def get_answer_service(user_repo=Depends(get_answer_repository)) -> AnswerService:
    return AnswerService(user_repo)
