from sqlalchemy import Column, String, Table

from .utils import metadata, base_columns


users = Table(
    "users",
    metadata,
    *base_columns(),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)
