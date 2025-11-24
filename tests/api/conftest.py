from unittest.mock import AsyncMock

import pytest

from app.__main__ import app
from app.api.dependencies import get_answer_service, get_question_service


@pytest.fixture()
def override_answer_service():
    mock_service = AsyncMock()
    app.dependency_overrides[get_answer_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()


@pytest.fixture()
def override_question_service():
    mock_service = AsyncMock()
    app.dependency_overrides[get_question_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides.clear()
