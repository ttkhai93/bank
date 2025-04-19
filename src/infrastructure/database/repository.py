from uuid import UUID

import sqlalchemy as sa
from arrow import Arrow

from .transaction import execute


class EntityRepository:
    entity: sa.Table

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "entity"):
            raise AttributeError(f"Class '{cls.__name__}' must define 'entity' class attribute")

    @staticmethod
    async def execute_sql_string(sql_string: str, **params):
        stmt = sa.text(sql_string).bindparams(**params)
        result = await execute(stmt)
        return _cursor_result_to_records(result)

    @classmethod
    async def get(
        cls,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
        for_update: bool = False,
        **column_filters,
    ):
        stmt = sa.select(cls.entity).filter_by(**column_filters)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        if order_by:
            if order_by.startswith("-"):
                column = order_by.removeprefix("-")
                stmt = stmt.order_by(sa.text(f"{column} DESC"))
            else:
                column = order_by
                stmt = stmt.order_by(sa.text(column))
        if for_update:
            stmt = stmt.with_for_update()
        result = await execute(stmt)
        return _cursor_result_to_records(result)

    @classmethod
    async def get_by_id(cls, record_id: UUID, for_update: bool = False) -> dict | None:
        records = await cls.get(id=record_id, for_update=for_update)
        if records:
            return records[0]
        return None

    @classmethod
    async def create(cls, values: dict):
        records = await cls.create_many(values)
        return records[0]

    @classmethod
    async def create_many(cls, values: dict | list[dict]):
        stmt = sa.insert(cls.entity).values(values).returning(*cls.entity.columns.values())
        result = await execute(stmt)
        return _cursor_result_to_records(result)

    @classmethod
    async def update(cls, values: dict, **column_filters):
        stmt = sa.update(cls.entity).values(values).filter_by(**column_filters).returning(*cls.entity.columns.values())
        result = await execute(stmt)
        return _cursor_result_to_records(result)

    @classmethod
    async def archive(cls, **column_filters):
        records = await cls.update({"archived": True}, **column_filters)
        return records


def _cursor_result_to_records(result):
    records = [dict(zip(result.keys(), row)) for row in result]
    for record in records:
        for field, value in record.items():
            if isinstance(value, Arrow):
                record[field] = value.isoformat()
    return records
