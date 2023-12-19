import datetime
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
    print(await dbTools.view_dat_row("./source/world.db", "world_chats", "id", "1"))


if __name__ == '__main__':
    print(datetime.datetime.now())
    run(g())




#
#    @commands.Cog.listener()
#    async def on_message(self, message):
#        if message.author.bot:
#            return
#        db = await dbTools.get_DB_path()
#        print(message.channel.id)
#        data = await dbTools.view_data(db, "world_chats", "channel_id", message.channel.id)
#        if data:
#            webhook = await self.get_webhook(message.channel.id)
#            if webhook:
#                async with self.webhook_session.post(webhook.url, json={"content": message.content,
#                                                                        "username": message.author.name,
#                                                                        "avatar_url": message.author.avatar_url}) as response:
#                    pass
#