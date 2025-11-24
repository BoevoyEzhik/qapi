from datetime import datetime

from httpx import AsyncClient

from app.models.question import Question

mock_question = Question(
    id=1, text="Test question", created_at=datetime(2025, 1, 1, 0, 0, 0)
)


async def test_get_questions_success(
    async_client: AsyncClient, override_question_service
):
    mock_questions = [
        {"id": 1, "text": "First question", "created_at": "2024-01-01T00:00:00"},
        {"id": 2, "text": "Second question", "created_at": "2024-01-01T00:00:00"},
    ]

    override_question_service.get_all_questions.return_value = mock_questions

    response = await async_client.get("/questions/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["text"] == "First question"
    assert data[1]["text"] == "Second question"

    override_question_service.get_all_questions.assert_called_once()


async def test_get_questions_empty_list(
    async_client: AsyncClient, override_question_service
):
    override_question_service.get_all_questions.return_value = []

    response = await async_client.get("/questions/")

    assert response.status_code == 200
    data = response.json()
    assert data == []

    override_question_service.get_all_questions.assert_called_once()


async def test_get_question_by_id_success(
    async_client: AsyncClient, override_question_service
):

    override_question_service.get_question_by_id.return_value = mock_question

    response = await async_client.get("/questions/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["text"] == "Test question"
    override_question_service.get_question_by_id.assert_called_once_with(1)


async def test_get_question_by_id_not_found(
    async_client: AsyncClient, override_question_service
):
    override_question_service.get_question_by_id.return_value = None

    response = await async_client.get("/questions/999")

    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Question not found"
    override_question_service.get_question_by_id.assert_called_once_with(999)


async def test_get_question_by_id_invalid_id(
    async_client: AsyncClient, override_question_service
):
    response = await async_client.get("/questions/abc")

    assert response.status_code == 422
    override_question_service.get_question_by_id.assert_not_called()


async def test_post_question_success(
    async_client: AsyncClient, override_question_service
):

    override_question_service.create_question.return_value = mock_question

    valid_data = {"text": "Test question"}

    response = await async_client.post("/questions/", json=valid_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["text"] == "Test question"
    override_question_service.create_question.assert_called_once()


async def test_post_question_empty_text(
    async_client: AsyncClient, override_question_service
):
    invalid_data = {"text": ""}

    response = await async_client.post("/questions/", json=invalid_data)

    assert response.status_code == 422
    override_question_service.create_question.assert_not_called()


async def test_post_question_whitespace_text(
    async_client: AsyncClient, override_question_service
):
    invalid_data = {"text": "   "}

    response = await async_client.post("/questions/", json=invalid_data)

    assert response.status_code == 422
    override_question_service.create_question.assert_not_called()


async def test_post_question_missing_text(
    async_client: AsyncClient, override_question_service
):
    response = await async_client.post("/questions/", json={})

    assert response.status_code == 422
    override_question_service.create_question.assert_not_called()


async def test_delete_question_success(
    async_client: AsyncClient, override_question_service
):
    override_question_service.delete_question.return_value = True

    response = await async_client.delete("/questions/1")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Question deleted"
    override_question_service.delete_question.assert_called_once_with(1)


async def test_delete_question_not_found(
    async_client: AsyncClient, override_question_service
):
    override_question_service.delete_question.return_value = False

    response = await async_client.delete("/questions/999")

    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Question not found"
    override_question_service.delete_question.assert_called_once_with(999)
