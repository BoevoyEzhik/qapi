import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import AnswerService, get_answer_service
from app.schemas.answers import AnswerCreate, AnswerResponse

logger = logging.getLogger(__name__)

answer_router = APIRouter(prefix="", tags=["answers"])


@answer_router.get("/answers/{id}", response_model=AnswerResponse)
async def get_answer(
    id: int, answer_service: AnswerService = Depends(get_answer_service)
):
    logger.info(f"Запрос на получение ответа с id={id}")
    answer = await answer_service.get_answer(id)
    if not answer:
        logger.warning(f"Ответ с id={id} не найден")
        raise HTTPException(status_code=404, detail="Answer not found")
    logger.info(f"Ответ с id={id} успешно возвращён")
    return answer


@answer_router.post("/questions/{id}/answers/", response_model=AnswerResponse)
async def post_answer(
    id: int,
    answer_schema: AnswerCreate,
    answer_service: AnswerService = Depends(get_answer_service),
):
    logger.info(f"Создание ответа для вопроса с id={id}")
    answer = await answer_service.create_answer(id, answer_schema)
    if not answer:
        logger.warning(f"Не удалось создать ответ: вопрос с id={id}")
        raise HTTPException(status_code=404, detail="Question not found")
    logger.info(f"Ответ успешно создан для вопроса id={id}")
    return answer


@answer_router.delete("/answers/{id}")
async def delete_answer(
    id: int, answer_service: AnswerService = Depends(get_answer_service)
):
    logger.info(f"Запрос на удаление ответа с id={id}")
    success = await answer_service.delete_answer(id)
    if not success:
        logger.warning(f"Не удалось удалить ответ с id={id}: не найден")
        raise HTTPException(status_code=404, detail="Answer not found")
    logger.info(f"Ответ с id={id} успешно удалён")
    return {"message": "Answer deleted successfully"}
