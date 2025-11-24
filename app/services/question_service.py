from app.repositories.question_repository import QuestionRepository
from app.schemas.questions import QuestionCreate


class QuestionService:
    def __init__(self, question_repo: QuestionRepository):
        self.question_repo = question_repo

    async def get_all_questions(self):
        return await self.question_repo.get_all_questions()

    async def get_question_by_id(self, question_id: int):
        return await self.question_repo.get_question_by_id_with_answers(question_id)

    async def create_question(self, question_schema: QuestionCreate):
        return await self.question_repo.create_question(question_schema.text)

    async def delete_question(self, question_id: int):
        return await self.question_repo.delete_question(question_id)
