import sqlalchemy as sa
from sqlalchemy.sql.base import Executable


def select(
    entity: sa.Table,
    offset: int = None,
    limit: int = None,
    order_by: str = None,
    for_update: bool = False,
    **column_filters,
) -> Executable:
    stmt = sa.select(entity).filter_by(**column_filters)
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

    return stmt


def insert(entity: sa.Table, values: dict | list[dict]) -> Executable:
    return sa.insert(entity).values(values).returning(*entity.columns.values())


def update(entity: sa.Table, values: dict, **column_filters) -> Executable:
    return sa.update(entity).values(values).filter_by(**column_filters).returning(*entity.columns.values())
