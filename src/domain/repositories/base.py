from typing import Any
from uuid import UUID

from sqlalchemy import Table, select, insert, update, text

from src.infrastructure.database import transaction


class BaseRepository:
    entity: Table = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.entity is None:
            raise AttributeError(f"Class '{cls.__name__}' must define 'table' class attribute")

    @classmethod
    async def get(
        cls,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
        for_update: bool = False,
        **column_filters,
    ):
        stmt = select(cls.entity).filter_by(**column_filters)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        if order_by:
            if order_by.startswith("-"):
                column = order_by.removeprefix("-")
                stmt = stmt.order_by(text(f"{column} DESC"))
            else:
                column = order_by
                stmt = stmt.order_by(text(column))
        if for_update:
            stmt = stmt.with_for_update()
        records = await transaction.execute(stmt)
        return records

    @classmethod
    async def get_by_id(cls, record_id: UUID, for_update: bool = False) -> dict | None:
        records = await cls.get(id=record_id, for_update=for_update)
        if records:
            return records[0]
        return None

    @classmethod
    async def create(cls, values: dict[str, Any]):
        stmt = insert(cls.entity).values(values).returning(*cls.entity.columns.values())
        records = await transaction.execute(stmt)
        return records[0]

    @classmethod
    async def create_many(cls, list_values: list[dict[str, Any]]):
        stmt = insert(cls.entity).values(list_values).returning(*cls.entity.columns.values())
        records = await transaction.execute(stmt)
        return records

    @classmethod
    async def update(cls, values: dict[str, Any], **column_filters):
        stmt = update(cls.entity).values(values).filter_by(**column_filters).returning(*cls.entity.columns.values())
        records = await transaction.execute(stmt)
        return records

    @classmethod
    async def archive(cls, **column_filters):
        records = await cls.update({"archived": True}, **column_filters)
        return records
