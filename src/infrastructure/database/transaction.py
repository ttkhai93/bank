from typing import Any
from contextvars import ContextVar
from contextlib import asynccontextmanager

from sqlalchemy import Executable, CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from . import Engine

_ctx_conn: ContextVar[AsyncConnection | None] = ContextVar("CTX_CONNECTION", default=None)


@asynccontextmanager
async def context(**execution_options):
    conn = Engine.get(**execution_options).connect()

    async with conn:
        token = _ctx_conn.set(conn)

        async with conn.begin():
            yield conn

        _ctx_conn.reset(token)


async def execute(statement: Executable) -> CursorResult[Any]:
    """
    This function executes a database operation inside a transaction.

    If context connection exists, this operation is supposed to belong to a transaction.
    So, it uses the current connection to execute the operation to ensure transaction atomicity

    Otherwise, it creates a new transaction that executes a single operation
    :param statement: The statement to be executed
    :return: List of database records
    """
    conn = _ctx_conn.get()
    if conn:
        return await conn.execute(statement)

    async with context() as conn:
        return await conn.execute(statement)
