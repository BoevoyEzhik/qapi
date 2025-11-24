from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.question import Question


class QuestionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_questions(self) -> Sequence[Question]:
        result = await self.session.execute(select(Question))
        return result.scalars().all()

    async def get_question_by_id_with_answers(
        self, question_id: int
    ) -> Question | None:
        query = (
            select(Question)
            .options(joinedload(Question.answers))
            .where(Question.id == question_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_question(self, text: str) -> Question:
        question = Question(text=text)
        self.session.add(question)
        await self.session.commit()
        return question

    async def delete_question(self, question_id: int):
        question = await self.session.get(Question, question_id)
        if not question:
            return False
        await self.session.delete(question)
        await self.session.commit()
        return True
