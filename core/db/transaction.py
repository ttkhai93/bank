from contextvars import ContextVar

from sqlalchemy import CursorResult, Executable
from sqlalchemy.ext.asyncio import AsyncConnection

from . import engine


ctx_connection = ContextVar("CTX_CONNECTION", default=None)


class Transaction:
    def __init__(self, **execution_options):
        self.execution_options = execution_options
        self.ctx_token = None

    async def create_connection(self):
        connection = await engine.get().connect()
        connection = await connection.execution_options(**self.execution_options)
        return connection

    async def __aenter__(self) -> AsyncConnection:
        connection = await self.create_connection()
        self.ctx_token = ctx_connection.set(connection)

        await connection.begin()
        return connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        connection: AsyncConnection = ctx_connection.get()
        if exc_type is None:
            await connection.commit()
        else:
            await connection.rollback()

        await connection.close()
        ctx_connection.reset(self.ctx_token)


async def execute(statement: Executable) -> CursorResult:
    connection: AsyncConnection | None = ctx_connection.get()
    if connection:
        return await connection.execute(statement)

    async with Transaction():
        return await execute(statement)
