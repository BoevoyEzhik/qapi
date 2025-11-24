import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import QuestionService, get_question_service
from app.schemas.questions import (
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswersResponse,
)

logger = logging.getLogger(__name__)

questions_router = APIRouter(prefix="/questions", tags=["questions"])


@questions_router.get("/")
async def get_questions(
    question_service: QuestionService = Depends(get_question_service),
):
    logger.info("Получение списка всех вопросов")
    questions = await question_service.get_all_questions()
    logger.info(f"Возвращено {len(questions)} вопросов")
    return questions


@questions_router.get("/{id}", response_model=QuestionWithAnswersResponse)
async def get_questions_by_id(
    id: int, question_service: QuestionService = Depends(get_question_service)
):
    logger.info(f"Запрос на получение вопроса с id={id}")
    question = await question_service.get_question_by_id(id)
    if not question:
        logger.warning(f"Вопрос с id={id} не найден")
        raise HTTPException(status_code=404, detail="Question not found")
    logger.info(f"Вопрос с id={id} успешно возвращён")
    return question


@questions_router.post("/", response_model=QuestionResponse)
async def post_questions(
    question_schema: QuestionCreate,
    question_service: QuestionService = Depends(get_question_service),
):
    logger.info(f"Создание вопроса с текстом: {question_schema.text[:30]}")
    question = await question_service.create_question(question_schema)
    logger.info(f"Вопрос успешно создан с id={question.id}")
    return question


@questions_router.delete("/{id}")
async def delete_questions(
    id: int, question_service: QuestionService = Depends(get_question_service)
):
    logger.info(f"Запрос на удаление вопроса с id={id}")
    success = await question_service.delete_question(id)
    if not success:
        logger.info(f"вопрос с id={id} не найден")
        raise HTTPException(status_code=404, detail="Question not found")
    logger.info(f"вопрос с id={id} успешно удалён")
    return {"message": "Question deleted"}
