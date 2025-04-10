from sqlalchemy import MetaData, Column, Boolean, UUID, text
from sqlalchemy_utils import ArrowType

metadata = MetaData()
uuid_generate_v4 = text("uuid_generate_v4()")
now_at_utc = text("(now() at time zone 'utc')")


def base_columns():
    return (
        Column("id", UUID, primary_key=True, server_default=uuid_generate_v4),
        Column("created", ArrowType, nullable=False, server_default=now_at_utc),
        Column("updated", ArrowType, nullable=False, server_default=now_at_utc),
        Column("archived", Boolean, server_default="false"),
    )
