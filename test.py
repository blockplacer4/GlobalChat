from asyncio import run
from source import dbTools

data = {
    "id": "int",
    "channel_id": "int",
    "webhook_url": "char*"
}


async def main():
    await dbTools.create_database("test.db")
    await dbTools.create_table("test.db", "globalchat", "id, channel_id, webhook_url")


async def test():
    # await dbTools.insert_data("test.db", "globalchat", "1", "321", "discord.com")
    await dbTools.update_data("test.db", "globalchat", "1", "3", "123", "google.com")
    # row = await dbTools.view_data("test.db", "globalchat", 1)
    # print(row)


async def g():
    print(await dbTools.get_DC_token())


if __name__ == '__main__':
    print(data)
    run(g())
