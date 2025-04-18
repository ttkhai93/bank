from contextvars import ContextVar
from contextlib import asynccontextmanager

from sqlalchemy import Executable, text
from sqlalchemy.ext.asyncio import AsyncConnection

from . import engine, utils

_ctx_conn: ContextVar[AsyncConnection | None] = ContextVar("CTX_CONNECTION", default=None)


@asynccontextmanager
async def context(**execution_options):
    conn = engine.get(**execution_options).connect()

    async with conn:
        token = _ctx_conn.set(conn)

        async with conn.begin():
            yield conn

        _ctx_conn.reset(token)


async def execute(statement: Executable, **execution_options) -> list[dict]:
    conn = _ctx_conn.get()
    if conn:
        return utils.cursor_result_to_records(await conn.execute(statement))

    async with context(**execution_options) as conn:
        return utils.cursor_result_to_records(await conn.execute(statement))


async def execute_text_clause(sql_string: str, **params):
    statement = text(sql_string).bindparams(**params)
    return await execute(statement)
