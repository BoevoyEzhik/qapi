import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer import Answer
from app.models.question import Question


class AnswerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_answer_by_id(self, answer_id: int) -> Answer | None:
        return await self.session.get(Answer, answer_id)

    async def create_answer(
        self, question_id: int, user_id: uuid.UUID, text: str
    ) -> Answer | None:
        question_result = await self.session.execute(
            select(Question).where(Question.id == question_id)
        )
        question = question_result.scalars().first()
        if not question:
            return None

        answer = Answer(user_id=user_id, question_id=question_id, text=text)
        self.session.add(answer)
        await self.session.commit()
        return answer

    async def delete_answer(self, answer_id: int) -> bool:
        answer = await self.get_answer_by_id(answer_id)
        if not answer:
            return False
        await self.session.delete(answer)
        await self.session.commit()
        return True

