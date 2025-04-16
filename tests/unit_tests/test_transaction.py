from pytest import raises

from core.db import transaction
from core.db.transaction import _ctx_connection
from sqlalchemy import text

from ..utils import engine_context


async def test_use_transaction_context_manager(postgres_url):
    assert _ctx_connection.get() is None

    async with engine_context(postgres_url):
        async with transaction.context():
            await transaction.execute(text("SELECT 1"))
            assert _ctx_connection.get()

    assert _ctx_connection.get() is None


async def test_use_transaction_context_manager_without_engine():
    with raises(ValueError):
        async with transaction.context():
            pass


async def test_use_execute_function(postgres_url):
    assert _ctx_connection.get() is None

    async with engine_context(postgres_url):
        await transaction.execute(text("SELECT 1"))

    assert _ctx_connection.get() is None


async def test_use_execute_function_without_engine():
    with raises(ValueError):
        await transaction.execute(text("SELECT 1"))
