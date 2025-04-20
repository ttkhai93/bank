from uuid import UUID

import sqlalchemy as sa
from arrow import Arrow

from .transaction import execute


class EntityRepository:
    def __init__(self, entity: sa.Table):
        self.entity = entity

    async def execute_sql_string(self, sql_string: str, **params):
        stmt = sa.text(sql_string).bindparams(**params)
        result = await execute(stmt)
        return self._cursor_result_to_records(result)

    async def get(
        self,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
        for_update: bool = False,
        **column_filters,
    ):
        stmt = sa.select(self.entity).filter_by(**column_filters)
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
        return self._cursor_result_to_records(result)

    async def get_by_id(self, record_id: UUID, for_update: bool = False) -> dict | None:
        records = await self.get(id=record_id, for_update=for_update)
        if records:
            return records[0]
        return None

    async def create(self, values: dict):
        records = await self.create_many(values)
        return records[0]

    async def create_many(self, values: dict | list[dict]):
        stmt = sa.insert(self.entity).values(values).returning(*self.entity.columns.values())
        result = await execute(stmt)
        return self._cursor_result_to_records(result)

    async def update(self, values: dict, **column_filters):
        stmt = (
            sa.update(self.entity).values(values).filter_by(**column_filters).returning(*self.entity.columns.values())
        )
        result = await execute(stmt)
        return self._cursor_result_to_records(result)

    async def archive(self, **column_filters):
        records = await self.update({"archived": True}, **column_filters)
        return records

    @staticmethod
    def _cursor_result_to_records(result):
        records = [dict(zip(result.keys(), row)) for row in result]
        for record in records:
            for field, value in record.items():
                if isinstance(value, Arrow):
                    record[field] = value.isoformat()
        return records
