import aiosqlite
import asyncio
from configparser import ConfigParser
import os
import datetime
import schedule


async def clear_db():
    pass


async def get_DB_path():
    config = ConfigParser()
    config.read("./source/configuration.cfg")
    if not config.has_section("DB") or not config.has_option("DB", "db_path"):
        if not config.has_section("DB"): config.add_section("DB")
        config['DB'] = {
            'db_path': './source/world.db'
        }
        with open('configuration.cfg', 'w') as config_file:
            config.write(config_file)
    db_path = config["DB"]["db_path"]
    return db_path


async def get_DC_token():
    config = ConfigParser()
    config.read("./source/configuration.cfg")
    if not config.has_section("BOT") or not config.has_option("BOT", "token"):
        config.add_section("BOT")
        config['BOT'] = {
            'token': '[REDACTED]'
        }
        with open('configuration.cfg', 'w') as config_file:
            config.write(config_file)
    token = config.get("BOT", "token")
    if token == "[REDACTED]":
        print("EDIT THE CONFIG FILE!!! TOKEN MISSING")
    return token


async def get_current_id(database_name, table_name):
    print(1)
    conn = await aiosqlite.connect(database_name)
    print(2)
    cursor = await conn.cursor()
    print(3)
    try:
        await cursor.execute(f"SELECT COUNT(*) FROM {table_name};")  # f"SELECT COUNT(*) FROM {table_name};"
    except Exception as e:
        print(e.with_traceback(e))
    print(4)
    try:
        next_id = await cursor.fetchall()
    except Exception as e:
        print(e.with_traceback(e))
        next_id = None
    print(f"5 {next_id[0]}")
    try:
        await conn.close()
        print(6)
        if next_id is None:
            print("[FAIL] dbTools.py")
        else:
            return next_id
    except ValueError as e:
        print(e.with_traceback(e))
        print(7)
    await conn.close()


async def get_next_id(database_name, table_name):
    print(1)
    conn = await aiosqlite.connect(database_name)
    print(2)
    cursor = await conn.cursor()
    print(3)
    try:
        await cursor.execute(f"SELECT COUNT(*) FROM {table_name};")  # f"SELECT COUNT(*) FROM {table_name};"
    except Exception as e:
        print(e.with_traceback(e))
    print(4)
    try:
        next_id = await cursor.fetchall()
    except Exception as e:
        print(e.with_traceback(e))
        next_id = None
    print(f"5 {next_id[0]}")
    try:
        await conn.close()
        print(6)
        if next_id is None:
            print("[FAIL] dbTools.py")
        else:
            next_number = next_id[0]
            print(f"- {next_number}")
            next_number = next_number[0]
            print(f"-- {next_number}")
            return next_number + 1
    except ValueError as e:
        print(e.with_traceback(e))
        print(7)
    await conn.close()


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


async def insert_data(database_name, table_name, id, channel_id, webhook_url):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    print(f'INSERT INTO {table_name} VALUES ({id}, {channel_id}, {webhook_url})')
    await cursor.execute(f"INSERT INTO {table_name} (id, channel_id, webhook_url) VALUES (?, ?, ?);",
                         (id, channel_id, webhook_url))
    await conn.commit()
    await cursor.close()
    await conn.close()


async def view_dat_row(database_name, table_name, column, id):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    print(f'SELECT * FROM {table_name} WHERE {column} = {str(id)}')
    await cursor.execute(f'SELECT * FROM {table_name} WHERE {column} = {str(id)}')
    rows = await cursor.fetchall()
    print(rows)
    await cursor.close()
    await conn.close()
    if not rows:
        return None
    else:
        return rows


async def view_data(database_name, table_name, column, value):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'SELECT * FROM {table_name} WHERE {column} = ?', (value,))
    rows = await cursor.fetchall()
    await cursor.close()
    await conn.close()
    if not rows:
        return None
    else:
        return rows


async def update_data(database_name, table_name, condition_id, id, channel_id, webhook_url):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'UPDATE {table_name} SET id=?, channel_id=?, webhook_url=? WHERE id=?',
                         (id, channel_id, webhook_url, condition_id))
    await conn.commit()
    await cursor.close()
    await conn.close()


async def delete_data(database_name, table_name, id):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'DELETE FROM {table_name} WHERE id={id}')
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
