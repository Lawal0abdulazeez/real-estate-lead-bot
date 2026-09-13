import pytest_asyncio
from app.db.session import engine


@pytest_asyncio.fixture(autouse=True)
async def dispose_engine_after_test():
    yield
    await engine.dispose()
