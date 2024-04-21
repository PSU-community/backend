import asyncio

from src.database.session import async_session_maker
from src.database.base import BaseTable


async def drop():
    async with async_session_maker() as s:
        for t in BaseTable.metadata.sorted_tables:
            s.execute(t.drop())


asyncio.run(drop())