from databases.core import Connection
import typing


async def get_data_source_id(connection: Connection, name: str) -> None|int:
    return await connection.fetch_val(
        "select id from data_source where name = :name", 
        {'name': name},
        column='id'
    )


async def add_data_source(connection: Connection, name: str) -> int:
    return await connection.execute(
        "insert into data_source (name) values (:name)",
        {'name': name}
    )


async def get_field_id(connection: Connection, name: str, source_id: int) -> None|int:
    return await connection.fetch_val(
        "select id from field where field_name = :name and source_id = :source_id", 
        {'name': name, 'source_id': source_id},
        column='id'
    )


async def add_field(connection: Connection, name: str, source_id: int) -> int:
    return await connection.execute(
        "insert into field (source_id, field_name) values (:source_id, :name)",
        {'name': name, 'source_id': source_id}
    )

async def add_records(connection: Connection, field_id: int, records: list[dict]) -> None:
    await connection.execute_many(
        "insert into data (field_id, field_value, date) values (:field_id, :value, :date)",
        list(map(lambda record: {**record, 'field_id': field_id}, records))
    )