import pytest
from core.db.transaction import Transaction, execute, _ctx_connection
from sqlalchemy import text

from .utils import ctx_engine


async def test_use_transaction_context_manager(postgres_url):
    assert _ctx_connection.get() is None

    async with ctx_engine(postgres_url):
        async with Transaction():
            await execute(text("SELECT 1"))
            assert _ctx_connection.get()

    assert _ctx_connection.get() is None


async def test_use_transaction_context_manager_without_engine():
    with pytest.raises(ValueError):
        async with Transaction():
            pass


async def test_use_execute_function(postgres_url):
    assert _ctx_connection.get() is None

    async with ctx_engine(postgres_url):
        await execute(text("SELECT 1"))

    assert _ctx_connection.get() is None


async def test_use_execute_function_without_engine():
    with pytest.raises(ValueError):
        await execute(text("SELECT 1"))
