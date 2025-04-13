from typing import Any
from uuid import UUID

from sqlalchemy import Table, select, insert, update, text
from arrow import Arrow

from ..db.transaction import execute


class BaseRepository:
    table: Table = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.table is None:
            raise AttributeError(f"Class '{cls.__name__}' must define 'table' class attribute")

    @staticmethod
    async def execute_text_clause(sql_string: str, **params):
        statement = text(sql_string).bindparams(**params)
        result = await execute(statement)
        return _result_to_dict(result)

    @classmethod
    async def get(
        cls,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
        for_update: bool = False,
        **column_filters,
    ):
        statement = select(cls.table).filter_by(**column_filters)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        if order_by:
            if order_by[:1] not in ["+", "-"]:
                statement = statement.order_by(order_by)
            else:
                column = order_by[1:]
                if order_by[:1] == "+":
                    statement = statement.order_by(text(f"{column}"))
                else:
                    statement = statement.order_by(text(f"{column} DESC"))
        if for_update:
            statement = statement.with_for_update()

        result = await execute(statement)
        return _result_to_dict(result)

    @classmethod
    async def get_by_id(cls, record_id: UUID, for_update: bool = False) -> dict | None:
        records = await cls.get(id=record_id, for_update=for_update)
        if not records:
            return None
        return records[0]

    @classmethod
    async def create(cls, values: dict[str, Any]):
        statement = insert(cls.table).values(values).returning(*cls.table.columns.values())
        result = await execute(statement)
        return _result_to_dict(result)[0]

    @classmethod
    async def update(cls, values: dict[str, Any], **column_filters):
        statement = update(cls.table).values(values).filter_by(**column_filters).returning(*cls.table.columns.values())
        result = await execute(statement)
        return _result_to_dict(result)

    @classmethod
    async def archive(cls, **column_filters):
        return await cls.update({"archived": True}, **column_filters)


def _result_to_dict(result):
    records = [dict(zip(result.keys(), row)) for row in result]
    for record in records:
        for field, value in record.items():
            if isinstance(value, Arrow):
                record[field] = value.isoformat()
    return records
