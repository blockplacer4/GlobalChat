import sqlite3
import aiosqlite
from configparser import ConfigParser
import datetime
import discord


async def create_embed(server_name: str, author_icon: str, title: str, description: str, icon: str, footer: dict = None,
                       fields: list = None, thumbnail_url: str = None):  # create_embed("Stupid Title", "Stupider
    # description", "Nope", filed1_title="")
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Colour.red(),
        timestamp=datetime.datetime.now()
    )
    print(server_name.split("https"))
    print(author_icon)
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    # embed.set_author(str(server_name.split("https")), "", str(author_icon))
    embed.set_author(name=server_name, icon_url=author_icon)
    if footer:
        footer_icon = footer.get("icon_url")
        footer_text = footer.get("text")
        embed.set_footer(text=footer_text, icon_url=footer_icon)
    icon, crap = icon.split("https")
    if icon:
        embed.set_image(url=str(icon))
    if fields:
        for field in fields:
            name = field.get('name')
            value = field.get('value')
            inline = field.get('inline', False)
            embed.add_field(name=name, value=value, inline=inline)
    if type(embed) is not discord.Embed:
        print("NOT AN EMBED")
    return embed


async def get_DB_path():
    config = ConfigParser()
    config.read("./source/configuration.cfg")
    if not config.has_section("DB") or not config.has_option("DB", "db_path"):
        if not config.has_section("DB"):
            config.add_section("DB")
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
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    try:
        await cursor.execute(f"SELECT COUNT(*) FROM {table_name};")  # f"SELECT COUNT(*) FROM {table_name};"
    except Exception as e:
        print(e.with_traceback(e))
    try:
        next_id = await cursor.fetchall()
    except Exception as e:
        print(e.with_traceback(e))
        next_id = None
    try:
        await conn.close()
        if next_id is None:
            print("[FAIL] tools.py")
        else:
            return next_id
    except ValueError as e:
        print(e.with_traceback(e))
    await conn.close()


async def get_next_id(database_name, table_name):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    try:
        await cursor.execute(f"SELECT COUNT(*) FROM {table_name};")  # f"SELECT COUNT(*) FROM {table_name};"
    except Exception as e:
        print(e.with_traceback(e))
    try:
        next_id: list = await cursor.fetchall()
    except Exception as e:
        print(e.with_traceback(e))
        next_id = None
    try:
        await conn.close()
        if next_id is None:
            print("[FAIL] tools.py")
        else:
            try:
                next_number = next_id[0]
                next_number = next_number[0]
                return next_number + 1
            except Exception as e:
                print(e.with_traceback(e))
    except ValueError as e:
        print(e.with_traceback(e))
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


async def insert_data(database_name, table_name, ident, channel_id, webhook_url, guild_id):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f"INSERT INTO {table_name} (id, channel_id, webhook_url, guild_id) VALUES (?, ?, ?, ?);",
                         (ident, channel_id, webhook_url, guild_id))
    await conn.commit()
    await cursor.close()
    await conn.close()


async def view_dat_row(database_name, table_name, column, ident):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'SELECT * FROM {table_name} WHERE {column} = {str(ident)}')
    rows = await cursor.fetchall()
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


async def update_data(database_name: str, table_name: str, condition_id: int, new_id: int, channel_id: int,
                      webhook_url: str):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'UPDATE {table_name} SET id=?, channel_id=?, webhook_url=? WHERE id=?',
                         (new_id, channel_id, webhook_url, condition_id))
    await conn.commit()
    await cursor.close()
    await conn.close()


async def get_column(database_name: str, table_name: str, column: str):
    print(1)
    conn = await aiosqlite.connect(database_name)
    print(2)
    cursor = await conn.cursor()
    print(3)
    try:
        print(4)
        await cursor.execute(f'SELECT {column} FROM {table_name}')
        print(5)
    except sqlite3.OperationalError:
        print(4)
        print("Sqlite get column Failed")
        print(5)
    print(6)
    data = await cursor.fetchall()
    print(7)
    await conn.commit()
    print(8)
    await cursor.close()
    print(9)
    await conn.close()
    print(10)
    if not data:
        print(11)
        print("There are no channels")
        print(12)
    else:
        print(11)
        return data


async def delete_data(database_name, table_name, ident):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'DELETE FROM {table_name} WHERE channel_id={ident}')
    await conn.commit()
    await cursor.close()
    await conn.close()


async def delete_server_data(database_name, table_name, guild_id):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    await cursor.execute(f'DELETE FROM {table_name} WHERE guild_id={guild_id}')
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
