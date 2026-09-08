"""Quick helper to create all tables without Alembic (dev only)."""
import asyncio

from app.db.base import Base
from app.db.session import engine
from app.models import Activity, Conversation, Lead, LeadScore, Message  # noqa: F401


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
