from pytest import raises

from core.db import engine
from ..utils import engine_context


async def test_engine_lifecycle(postgres_url):
    async with engine_context(postgres_url):
        assert engine.get()


async def test_create_engine_when_already_created(postgres_url):
    async with engine_context(postgres_url):
        with raises(ValueError):
            engine.create(postgres_url)


async def test_get_engine_when_not_exists():
    with raises(ValueError):
        engine.get()


async def test_dispose_engine_when_not_exists():
    with raises(ValueError):
        await engine.dispose()
