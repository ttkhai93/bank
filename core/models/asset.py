from sqlalchemy import Column, String, Table

from .base import metadata, base_columns


asset = Table(
    "asset",
    metadata,
    *base_columns(),
    Column("code", String, unique=True, nullable=False),
    Column("name", String, nullable=False),
)
