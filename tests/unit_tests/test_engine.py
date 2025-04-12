import pytest
from core.db import engine
from ..utils import ctx_engine


async def test_get_engine(postgres_url):
    async with ctx_engine(postgres_url):
        assert engine.get()


async def test_create_engine_when_already_created(postgres_url):
    async with ctx_engine(postgres_url):
        with pytest.raises(ValueError):
            engine.create(postgres_url)


async def test_get_engine_when_not_exists():
    with pytest.raises(ValueError):
        engine.get()


async def test_dispose_engine_when_not_exists():
    with pytest.raises(ValueError):
        await engine.dispose()
