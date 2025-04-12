from sqlalchemy import Column, Table, ForeignKey, Numeric, text

from .base import metadata, base_columns


account = Table(
    "account",
    metadata,
    *base_columns(),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("asset_id", ForeignKey("asset.id"), nullable=False),
    Column("amount", Numeric(precision=24, scale=8), nullable=False, server_default=text("0")),
)
