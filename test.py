import datetime
from asyncio import run
from source import tools
import requests
data = {
    "id": "int",
    "channel_id": "int",
    "webhook_url": "char*"
}


async def main():
    await tools.create_table(await tools.get_DB_path(), "world_chats", "id, channel_id, webhook_url, guild_id")


async def test():
    # await dbTools.insert_data("test.db", "globalchat", "1", "321", "discord.com")
    await tools.update_data("test.db", "globalchat", "1", "3", "123", "google.com")
    # row = await dbTools.view_data("test.db", "globalchat", 1)
    # print(row)


async def g():
    print(await tools.view_dat_row("./source/world.db", "world_chats", "id", "1"))


if __name__ == '__main__':
    run(main())

fields = [
    {'name': 'Field 1', 'value': 'This is the first field'},
    {'name': 'Field 2', 'value': 'This is the second field'},
    {'name': 'Field 3', 'value': 'This is the third field', 'inline': True}
]