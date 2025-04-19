from pytest import raises

from src.infrastructure import Engine


async def test_engine_lifecycle(postgres_url):
    try:
        Engine.create(postgres_url)
        assert Engine.get()
    finally:
        await Engine.dispose()


async def test_create_engine_when_already_created(postgres_url):
    try:
        Engine.create(postgres_url)
        with raises(ValueError):
            Engine.create(postgres_url)
    finally:
        await Engine.dispose()


async def test_get_engine_when_not_exists():
    with raises(ValueError):
        Engine.get()
