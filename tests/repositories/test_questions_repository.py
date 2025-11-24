from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer import Answer
from app.models.question import Question
from app.repositories.question_repository import QuestionRepository


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def question_repository(mock_session):
    return QuestionRepository(session=mock_session)


async def test_get_all_questions(question_repository, mock_session):
    mock_questions = [
        MagicMock(spec=Question, id=1, text="Question 1"),
        MagicMock(spec=Question, id=2, text="Question 2"),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_questions
    mock_session.execute.return_value = mock_result

    result = await question_repository.get_all_questions()

    mock_session.execute.assert_awaited_once()
    executed_stmt = mock_session.execute.call_args[0][0]

    assert hasattr(executed_stmt, "_raw_columns")
    assert Question in [col.entity_namespace for col in executed_stmt._raw_columns]

    assert len(result) == 2
    assert result[0].text == "Question 1"
    assert result[1].text == "Question 2"


async def test_get_question_by_id_with_answers_success(question_repository, mock_session):
    mock_answers = [
        MagicMock(spec=Answer, id=1, text="Answer 1", user_id="user1"),
        MagicMock(spec=Answer, id=2, text="Answer 2", user_id="user2"),
    ]

    mock_question = MagicMock(spec=Question)
    mock_question.id = 1
    mock_question.text = "Test question"
    mock_question.answers = mock_answers

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_question
    mock_session.execute.return_value = mock_result

    result = await question_repository.get_question_by_id_with_answers(1)

    mock_session.execute.assert_awaited_once()
    executed_stmt = mock_session.execute.call_args[0][0]

    from sqlalchemy.sql.selectable import Select
    assert isinstance(executed_stmt, Select)
    assert Question in [col.entity_namespace for col in executed_stmt._raw_columns]

    assert result is not None
    assert result.id == 1
    assert result.text == "Test question"
    assert len(result.answers) == 2
    assert result.answers[0].text == "Answer 1"


async def test_get_question_by_id_with_answers_not_found(question_repository, mock_session):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result

    result = await question_repository.get_question_by_id_with_answers(999)

    mock_session.execute.assert_awaited_once()

    assert result is None


async def test_create_question_success(question_repository, mock_session):
    text = "Test question"

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    result = await question_repository.create_question(text)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

    call_args = mock_session.add.call_args[0][0]
    assert call_args.text == text
    assert result.text == text


async def test_delete_question_success(question_repository, mock_session):
    question_id = 1
    mock_question = MagicMock()

    mock_session.get = AsyncMock(return_value=mock_question)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    result = await question_repository.delete_question(question_id)

    mock_session.get.assert_awaited_once_with(Question, question_id)
    mock_session.delete.assert_awaited_once_with(mock_question)
    mock_session.commit.assert_awaited_once()
    assert result is True


async def test_delete_question_not_found(question_repository, mock_session):
    question_id = 999

    mock_session.get = AsyncMock(return_value=None)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    result = await question_repository.delete_question(question_id)

    mock_session.get.assert_awaited_once_with(Question, question_id)
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
    assert result is False