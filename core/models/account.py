from sqlalchemy import Column, Table, ForeignKey

from .base import metadata, base_columns


account = Table(
    "account",
    metadata,
    *base_columns(),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("asset_id", ForeignKey("asset.id"), nullable=False),
)
