import os
import asyncio

from asyncpg import connect, Connection
from pytest import fixture
from httpx import AsyncClient, ASGITransport
from alembic import command
from alembic.config import Config

from core.models.base import metadata
from settings import db_settings
from main import app
from .utils import working_directory


@fixture(scope="session")
def postgres_url(docker_services, docker_ip):
    host_port = docker_services.port_for("postgres", 5432)
    url = f"postgresql+asyncpg://postgres:postgres@{docker_ip}:{host_port}/postgres"

    def check_connection() -> Connection | None:
        try:
            return asyncio.run(connect(url.replace("+asyncpg", "")))
        except ConnectionError:
            return None

    docker_services.wait_until_responsive(check=check_connection, timeout=5, pause=0.5)
    return url


@fixture(scope="session", autouse=True)
def work_in_project_root():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with working_directory(project_root):
        yield


@fixture(scope="session", autouse=True)
def apply_migrations(postgres_url, work_in_project_root):
    """Apply migrations at beginning of test session"""
    db_settings.DATABASE_URL = postgres_url
    config = Config("alembic.ini")
    command.upgrade(config, "head")


@fixture(autouse=True)
async def reset_db(postgres_url: str):
    """Reset database after each test"""
    tables = ", ".join(metadata.tables.keys())
    sql = f"TRUNCATE TABLE {tables} CASCADE"

    connection: Connection = await connect(postgres_url.replace("+asyncpg", ""))
    await connection.execute(sql)


@fixture
async def new_client():
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
            yield client
