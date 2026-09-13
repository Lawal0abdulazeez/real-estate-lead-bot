"""Quick helper to create all tables without Alembic (dev only)."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine
from app.models import (  # noqa: F401
    Activity,
    Conversation,
    FollowUp,
    Lead,
    LeadScore,
    Message,
)


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Tables created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
