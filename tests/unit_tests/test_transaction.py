from pytest import raises

from core.db import engine
from core.db.transaction import Transaction, execute, _ctx_connection
from sqlalchemy import text


async def test_use_transaction_context_manager(postgres_url):
    assert _ctx_connection.get() is None

    async with engine.context(postgres_url):
        async with Transaction():
            await execute(text("SELECT 1"))
            assert _ctx_connection.get()

    assert _ctx_connection.get() is None


async def test_use_transaction_context_manager_without_engine():
    with raises(ValueError):
        async with Transaction():
            pass


async def test_use_execute_function(postgres_url):
    assert _ctx_connection.get() is None

    async with engine.context(postgres_url):
        await execute(text("SELECT 1"))

    assert _ctx_connection.get() is None


async def test_use_execute_function_without_engine():
    with raises(ValueError):
        await execute(text("SELECT 1"))
