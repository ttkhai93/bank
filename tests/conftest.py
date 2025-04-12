import os
import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from alembic import command
from alembic.config import Config

from core.models.base import metadata
from core.db.transaction import execute
from settings import settings
from .utils import working_directory, ctx_engine


@pytest.fixture(scope="session")
def postgres_url(docker_services, docker_ip):
    host_port = docker_services.port_for("postgres", 5432)
    url = f"postgresql+asyncpg://postgres:postgres@{docker_ip}:{host_port}/postgres"

    def check_connection() -> bool:
        try:

            async def check() -> bool:
                async with ctx_engine(url):
                    return bool(await execute(text("SELECT 1;")))

            return asyncio.run(check())
        except Exception:
            return False

    docker_services.wait_until_responsive(check=check_connection, timeout=5, pause=0.5)
    return url


@pytest.fixture(scope="session", autouse=True)
def test_settings(postgres_url):
    settings.DATABASE_URL = postgres_url


@pytest.fixture(scope="session", autouse=True)
def work_in_project_root():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with working_directory(project_root):
        yield


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(test_settings, work_in_project_root):
    """Apply migrations at beginning of test session"""
    config = Config("alembic.ini")
    command.upgrade(config, "head")


@pytest.fixture(scope="function")
async def new_client():
    from main import app

    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            yield client


@pytest.fixture(scope="function", autouse=True)
async def reset_db(postgres_url):
    """Reset database"""
    yield
    async with ctx_engine(postgres_url):
        for table in metadata.tables.keys():
            sql = f"TRUNCATE TABLE {table} CASCADE"
            await execute(text(sql))
