import os
import asyncio

from pytest import fixture
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from alembic import command
from alembic.config import Config

from core.models.base import metadata
from core.db import engine, transaction
from settings import db_settings
from main import app
from .utils import working_directory


@fixture(scope="session")
def postgres_url(docker_services, docker_ip):
    host_port = docker_services.port_for("postgres", 5432)
    url = f"postgresql+asyncpg://postgres:postgres@{docker_ip}:{host_port}/postgres"

    def check_connection() -> bool:
        try:

            async def check() -> bool:
                try:
                    engine.create(url)
                    return bool(await transaction.execute(text("SELECT 1;")))
                finally:
                    await engine.dispose()

            return asyncio.run(check())
        except Exception:
            return False

    docker_services.wait_until_responsive(check=check_connection, timeout=5, pause=0.5)
    return url


@fixture(scope="session", autouse=True)
def test_settings(postgres_url):
    db_settings.DATABASE_URL = postgres_url


@fixture(scope="session", autouse=True)
def work_in_project_root():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with working_directory(project_root):
        yield


@fixture(scope="session", autouse=True)
def apply_migrations(test_settings, work_in_project_root):
    """Apply migrations at beginning of test session"""
    config = Config("alembic.ini")
    command.upgrade(config, "head")


async def reset_db():
    """Reset database after each test"""
    tables = ", ".join(metadata.tables.keys())
    sql = f"TRUNCATE TABLE {tables} CASCADE"
    await transaction.execute(text(sql))


@fixture(scope="function")
async def new_client():
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            yield client
            await reset_db()
