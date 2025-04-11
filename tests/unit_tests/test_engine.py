import pytest
from core.db import engine


async def test_engine(postgres_url):
    with pytest.raises(ValueError):
        engine.get()  # Cannot get the engine because it hasn't been created

    try:
        engine.create(postgres_url)
        assert engine.get()  # Can get the engine now
    finally:
        await engine.dispose()

        with pytest.raises(ValueError):
            assert engine.get()  # Cannot get the engine because it has been disposed
