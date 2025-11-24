import uuid
from datetime import datetime

from httpx import AsyncClient


async def test_get_answer_found(override_answer_service, async_client: AsyncClient):
    user_id = str(uuid.uuid4())
    override_answer_service.get_answer.return_value = {
        "id": 1,
        "text": "Test answer",
        "question_id": 1,
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
    }

    response = await async_client.get("/answers/1")

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["text"] == "Test answer"
    override_answer_service.get_answer.assert_called_once_with(1)


async def test_get_answer_not_found(override_answer_service, async_client: AsyncClient):
    override_answer_service.get_answer.return_value = None

    response = await async_client.get("/answers/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Answer not found"}


async def test_post_answer_success(override_answer_service, async_client: AsyncClient):
    test_user_id = str(uuid.uuid4())
    question_id = 1
    request_data = {"text": "This is a test answer", "user_id": test_user_id}

    expected_response = {
        "id": 1,
        "text": "This is a test answer",
        "question_id": question_id,
        "user_id": test_user_id,
        "created_at": "2025-01-01T00:00:00",
    }

    override_answer_service.create_answer.return_value = expected_response

    response = await async_client.post(
        f"/questions/{question_id}/answers/", json=request_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["text"] == request_data["text"]

    override_answer_service.create_answer.assert_called_once()


async def test_post_answer_question_not_found(
    override_answer_service, async_client: AsyncClient
):
    override_answer_service.create_answer.return_value = None

    user_id = str(uuid.uuid4())
    response = await async_client.post(
        "/questions/999/answers/", json={"user_id": user_id, "text": "Answer text"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


async def test_post_answer_empty_text(
    async_client: AsyncClient, override_answer_service
):
    test_user_id = str(uuid.uuid4())

    invalid_data = {"text": "", "user_id": test_user_id}

    response = await async_client.post("/questions/1/answers/", json=invalid_data)

    assert response.status_code == 422
    error_data = response.json()

    assert "detail" in error_data
    errors = error_data["detail"]

    text_error = next(
        (error for error in errors if error["loc"] == ["body", "text"]), None
    )
    assert text_error is not None
    assert (
        "empty" in text_error["msg"].lower() or "required" in text_error["msg"].lower()
    )

    override_answer_service.create_answer.assert_not_called()


async def test_post_answer_none_user_id(
    async_client: AsyncClient, override_answer_service
):
    invalid_data = {"text": "Valid text", "user_id": ""}

    response = await async_client.post("/questions/1/answers/", json=invalid_data)

    assert response.status_code == 422
    override_answer_service.create_answer.assert_not_called()


async def test_post_answer_invalid_uuid(
    async_client: AsyncClient, override_answer_service
):
    invalid_data = {"text": "Valid text", "user_id": "not-a-uuid"}

    response = await async_client.post("/questions/1/answers/", json=invalid_data)

    assert response.status_code == 422
    override_answer_service.create_answer.assert_not_called()


async def test_delete_answer_success(
    override_answer_service, async_client: AsyncClient
):
    override_answer_service.delete_answer.return_value = True

    response = await async_client.delete("/answers/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Answer deleted successfully"}
    override_answer_service.delete_answer.assert_called_once_with(1)


async def test_delete_answer_not_found(
    override_answer_service, async_client: AsyncClient
):
    override_answer_service.delete_answer.return_value = False

    response = await async_client.delete("/answers/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Answer not found"}
