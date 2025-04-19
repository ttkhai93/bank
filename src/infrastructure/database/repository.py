from uuid import UUID

from sqlalchemy import Table

from . import transaction
from . import statements


class EntityRepository:
    entity: Table

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "entity"):
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
        stmt = statements.select(cls.entity, offset, limit, order_by, for_update, **column_filters)
        records = await transaction.execute(stmt)
        return records

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
        stmt = statements.insert(cls.entity, values)
        records = await transaction.execute(stmt)
        return records

    @classmethod
    async def update(cls, values: dict, **column_filters):
        stmt = statements.update(cls.entity, values, **column_filters)
        records = await transaction.execute(stmt)
        return records

    @classmethod
    async def archive(cls, **column_filters):
        records = await cls.update({"archived": True}, **column_filters)
        return records
