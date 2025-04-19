from enum import StrEnum

from sqlalchemy import Column, Table, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import ENUM

from .utils import metadata, base_columns, get_enum_values


class TransactionStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    FAILED = "failed"


transaction = Table(
    "transaction",
    metadata,
    *base_columns(),
    Column("from_account_id", ForeignKey("account.id"), nullable=False),
    Column("to_account_id", ForeignKey("account.id"), nullable=False),
    Column("amount", Numeric(precision=24, scale=8), nullable=False),
    Column(
        "status",
        ENUM(TransactionStatus, name="transaction_status", values_callable=get_enum_values),
        nullable=False,
        server_default=TransactionStatus.PENDING,
    ),
)
