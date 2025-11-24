# Активируем поддержку асинхронных фикстур и тестов
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.__main__ import app

pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
