from sqlalchemy import text
from pytest import raises

from src.infrastructure import Engine, transaction


async def test_use_context_manager(postgres_url):
    assert transaction._ctx_conn.get() is None

    try:
        Engine.create(postgres_url)
        async with transaction.context():
            await transaction.execute(text("SELECT 1"))
            assert transaction._ctx_conn.get()
    finally:
        await Engine.dispose()

    assert transaction._ctx_conn.get() is None


async def test_use_context_manager_without_engine_fail():
    with raises(ValueError):
        async with transaction.context():
            pass


async def test_use_execute_function(postgres_url):
    assert transaction._ctx_conn.get() is None

    try:
        Engine.create(postgres_url)
        await transaction.execute(text("SELECT 1"))
    finally:
        await Engine.dispose()

    assert transaction._ctx_conn.get() is None


async def test_use_execute_function_without_engine():
    with raises(ValueError):
        await transaction.execute(text("SELECT 1"))
