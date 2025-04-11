import os
import asyncio

from sqlalchemy import text
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config
import pytest

from core.db import engine
from settings import settings
from core.models.base import metadata
from .utils import working_directory
from core.db.transaction import Transaction


@pytest.fixture(scope="session")
def postgres_url(docker_services, docker_ip):
    host_port = docker_services.port_for("postgres", 5432)
    url = f"postgresql+asyncpg://postgres:postgres@{docker_ip}:{host_port}/postgres"

    def check_connection() -> bool:
        try:

            async def check() -> bool:
                result = False
                try:
                    engine.create(url)
                    async with Transaction():
                        result = True
                finally:
                    await engine.dispose()
                    return result

            return asyncio.run(check())
        except Exception:
            return False

    docker_services.wait_until_responsive(check=check_connection, timeout=5, pause=0.1)
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
def apply_migrations(test_settings):
    """Apply migrations at beginning of test session"""
    config = Config("alembic.ini")
    command.upgrade(config, "head")


@pytest.fixture(scope="function")
def test_client():
    from main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
async def reset_db(postgres_url):
    """Reset database"""
    yield
    try:
        engine.create(postgres_url)
        async with Transaction() as conn:
            for table in metadata.tables.keys():
                sql = f"TRUNCATE TABLE {table} CASCADE"
                await conn.execute(text(sql))
    finally:
        await engine.dispose()
