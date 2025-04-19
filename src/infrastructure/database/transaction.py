from contextvars import ContextVar
from contextlib import asynccontextmanager

from sqlalchemy import Executable, text
from sqlalchemy.ext.asyncio import AsyncConnection
from arrow import Arrow

from . import engine

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
    # If context connection exists, this operation is supposed to belong to a transaction.
    # So, use the current connection to execute the operation to ensure transaction atomicity
    if conn:
        return _cursor_result_to_records(await conn.execute(statement))

    # Create a new transaction that executes a single operation
    async with context(**execution_options) as conn:
        return _cursor_result_to_records(await conn.execute(statement))


async def execute_text_clause(sql_string: str, **params):
    statement = text(sql_string).bindparams(**params)
    return await execute(statement)


def _cursor_result_to_records(result):
    records = [dict(zip(result.keys(), row)) for row in result]
    for record in records:
        for field, value in record.items():
            if isinstance(value, Arrow):
                record[field] = value.isoformat()
    return records
