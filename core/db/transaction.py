from contextvars import ContextVar

from sqlalchemy import CursorResult, Executable
from sqlalchemy.ext.asyncio import AsyncConnection

from . import engine

_ctx_connection = ContextVar("CTX_CONNECTION", default=None)


class Transaction:
    def __init__(self, **execution_options):
        self.execution_options = execution_options
        self.ctx_token = None

    async def __aenter__(self) -> AsyncConnection:
        connection = await engine.get_connection(**self.execution_options)
        self.ctx_token = _ctx_connection.set(connection)

        await connection.begin()
        return connection

    async def __aexit__(self, exc_type: type[Exception] | None, exc_val: Exception | None, exc_tb):
        connection: AsyncConnection = _ctx_connection.get()
        if exc_type is None:
            await connection.commit()
        else:
            await connection.rollback()

        await connection.close()
        _ctx_connection.reset(self.ctx_token)


async def execute(statement: Executable) -> CursorResult:
    connection: AsyncConnection | None = _ctx_connection.get()
    if connection:
        return await connection.execute(statement)

    async with Transaction():
        return await execute(statement)
