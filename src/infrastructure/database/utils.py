from arrow import Arrow


def cursor_result_to_records(result):
    records = [dict(zip(result.keys(), row)) for row in result]
    for record in records:
        for field, value in record.items():
            if isinstance(value, Arrow):
                record[field] = value.isoformat()
    return records
