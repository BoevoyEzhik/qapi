from app.repositories.answer_repository import AnswerRepository
from app.schemas.answers import AnswerCreate


class AnswerService:
    def __init__(self, answer_repo: AnswerRepository):
        self.answer_repo = answer_repo

    async def get_answer(self, answer_id):
        return await self.answer_repo.get_answer_by_id(answer_id)

    async def create_answer(self, question_id: int, answer_schema: AnswerCreate):
        return await self.answer_repo.create_answer(
            question_id, answer_schema.user_id, answer_schema.text
        )

    async def delete_answer(self, answer_id) -> bool:
        return await self.answer_repo.delete_answer(answer_id)
