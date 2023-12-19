import aiosqlite
import asyncio


async def create_database(database_name):
    conn = await aiosqlite.connect(database_name)
    await conn.close()


async def create_table(database_name, table_name, *columns):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    column_def = ', '.join(f'{column} TEXT' for column in columns)
    await cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_def})')
    await conn.commit()
    await cursor.close()
    await conn.close()


async def insert_data(database_name, table_name, *data):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    placeholders = ', '.join('?' * len(data))
    values = tuple(data)
    await cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', values)
    await conn.commit()
    await cursor.close()
    await conn.close()


async def view_data(database_name, table_name):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'SELECT * FROM {table_name}')
    rows = await cursor.fetchall()
    await cursor.close()
    await conn.close()
    return rows


async def update_data(database_name, table_name, condition, *data):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    placeholders = ', '.join('?' * len(data))
    values = tuple(data)
    await cursor.execute(f'UPDATE {table_name} SET {placeholders} WHERE {condition}', values)
    await conn.commit()
    await cursor.close()
    await conn.close()


async def delete_data(database_name, table_name, condition):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'DELETE FROM {table_name} WHERE {condition}')
    await conn.commit()
    await cursor.close()
    await conn.close()


async def execute_script(database_name, script):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.executescript(script)
    await conn.commit()
    await cursor.close()
    await conn.close()
