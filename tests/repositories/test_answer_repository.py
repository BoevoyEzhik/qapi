import uuid
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.answer import Answer
from app.repositories.answer_repository import AnswerRepository


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def answer_repository(mock_session):
    return AnswerRepository(session=mock_session)


async def test_get_answer_by_id_found(answer_repository, mock_session):
    answer_id = 1
    mock_answer = MagicMock()

    mock_session.get = AsyncMock(return_value=mock_answer)

    result = await answer_repository.get_answer_by_id(answer_id)

    mock_session.get.assert_awaited_once_with(Answer, answer_id)
    assert result is mock_answer


async def test_get_answer_by_id_not_found(answer_repository, mock_session):
    answer_id = 999

    mock_session.get = AsyncMock(return_value=None)

    result = await answer_repository.get_answer_by_id(answer_id)

    mock_session.get.assert_awaited_once_with(Answer, answer_id)
    assert result is None


async def test_create_answer_success(answer_repository, mock_session):
    question_id = 1
    user_id = uuid.uuid4()
    text = "Test answer"
    mock_question = MagicMock()
    mock_answer = MagicMock()

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_question
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    result = await answer_repository.create_answer(question_id, user_id, text)

    mock_session.execute.assert_awaited_once()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    assert result is not None


async def test_create_answer_question_not_found(answer_repository, mock_session):
    question_id = 999
    user_id = uuid.uuid4()
    text = "Test answer"

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    result = await answer_repository.create_answer(question_id, user_id, text)

    mock_session.execute.assert_awaited_once()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    assert result is None


async def test_delete_answer_success(answer_repository, mock_session):
    answer_id = 1
    mock_answer = MagicMock()

    answer_repository.get_answer_by_id = AsyncMock(return_value=mock_answer)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    result = await answer_repository.delete_answer(answer_id)

    answer_repository.get_answer_by_id.assert_awaited_once_with(answer_id)
    mock_session.delete.assert_awaited_once_with(mock_answer)
    mock_session.commit.assert_awaited_once()
    assert result is True


async def test_delete_answer_not_found(answer_repository, mock_session):
    answer_id = 999

    answer_repository.get_answer_by_id = AsyncMock(return_value=None)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    result = await answer_repository.delete_answer(answer_id)

    answer_repository.get_answer_by_id.assert_awaited_once_with(answer_id)
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
    assert result is False