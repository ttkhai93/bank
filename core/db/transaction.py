from contextvars import ContextVar
from contextlib import asynccontextmanager

from sqlalchemy import CursorResult, Executable
from sqlalchemy.ext.asyncio import AsyncConnection

from . import engine

_ctx_connection = ContextVar("CTX_CONNECTION", default=None)


@asynccontextmanager
async def context(**execution_options):
    conn = engine.get(**execution_options).connect()

    async with conn:
        token = _ctx_connection.set(conn)

        async with conn.begin():
            yield conn

        _ctx_connection.reset(token)


async def execute(statement: Executable) -> CursorResult:
    conn: AsyncConnection | None = _ctx_connection.get()
    if conn:
        return await conn.execute(statement)

    async with context() as conn:
        return await conn.execute(statement)
