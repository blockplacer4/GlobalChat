import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncpg
import aiohttp
from discord import Webhook
import run
from source import tools
from configparser import ConfigParser
import os
from urllib.parse import urlparse


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_session = aiohttp.ClientSession()

    async def send_global_message(self, server_name: str, author_icon: str, message: str, author: str, avatar_url: str, footer: dict, fields: list, thumbnail_url: str = None):
        for url in await tools.get_colummn("./source/world.db", "world_chats", "webhook_url"):
            webhook = Webhook.from_url(str(url), session=self.webhook_session)
            e = await tools.create_embed(server_name, author_icon, author, message, avatar_url, footer, fields, thumbnail_url)
            a = e.copy()
            await webhook.send(embed=e, avatar_url="https://i.ibb.co/D96qZq7/KH75-World-Chat-2.png")

    async def get_webhook(self, channel_id):
        try:
            print(1)
            channel = self.bot.get_channel(channel_id)
            print(2)
            if not channel:
                print("NO channel")
                return None
            print(3)
            webhooks = await channel.webhooks()
            print(4)
            webhook = discord.utils.get(webhooks, name="GlobalChat")
            print(5)
            if not webhook:
                print("Webhook existiert nicht")
                webhook = await channel.create_webhook(name="GlobalChat", avatar="https://i.ibb.co/D96qZq7/KH75-World-Chat-2.png")
                print(webhook.url)
                return webhook.url
                #async with aiohttp.ClientSession() as session:
                #    async with session.get("https://i.ibb.co/D96qZq7/KH75-World-Chat-2.png") as resp:
                #        if resp.status == 200:
                #            data = await resp.read()
                #            webhook = await channel.create_webhook(name="GlobalChat")
                #        else:
                #            return None
            return webhook.url
        except Exception as e:
            print(e.with_traceback(e))

    async def deletewebhook(self, channel_id):
        try:
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return None
            webhooks = await channel.webhooks()
            globalhook = None
            for webhook in webhooks:
                if webhook.name == "GlobalChat":
                    globalhook = webhook
                    break
            if globalhook:
                await globalhook.delete()
        except Exception as e:
            print(e.with_traceback(e))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("No Permission, yk yk.")

    @discord.slash_command()
    async def addglobal(self, ctx, channel: discord.TextChannel):
        print(channel.name)
        # async with self.bot.pool.acquire() as conn:
        if await tools.view_dat_row(await tools.get_DB_path(), "world_chats", "channel_id", channel.id):
            print("1")
            await ctx.respond(
                f"{channel.mention} ist bereits ein global chat zum entfernen benutze /removeglobal <channel>")
        else:
            webhook = await self.get_webhook(channel.id)
            print(webhook)
            try:
                db = await tools.get_DB_path()
                id = await tools.get_next_id(db, "world_chats")
                await tools.insert_data(db, "world_chats", id, channel.id, webhook)
                await ctx.respond(f"{channel.mention} wurde zum Global Chat hinzugefügt.")
            except Exception as e:
                print(e.with_traceback(e))

    @discord.slash_command()
    async def removeglobal(self, ctx, channel: discord.TextChannel):
        # async with self.bot.pool.acquire() as conn:
        db = await tools.get_DB_path()
        await tools.delete_data(db, "world_chats", f"{channel.id}")
        await self.deletewebhook(channel.id)
        await ctx.respond(f"{channel.mention} wurde vom Global Chat entfernt.")

    @discord.slash_command()
    async def help(self, ctx):
        ctx.respond(f"HELP")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            for channel_id in await tools.get_colummn(await tools.get_DB_path(), "world_chats", "channel_id"):
                if int(channel_id[0]) == message.channel.id:
                    db = await tools.get_DB_path()
                    footer = {
                        "icon_url": self.bot.user.avatar,
                        "text": f"Server anzahl: {await run.get_server_count()}"
                    }
                    fields = [
                        {'name': '', 'value': '🤖 [Invite mich](https://world.killerhase75.com)', 'inline': True}
                    ]
                    print(message.guild.icon)
                    if message.author.avatar:
                        await self.send_global_message(message.guild.name, message.guild.icon, message.content,
                                                       message.author.display_name, message.author.avatar.url, footer,
                                                       fields, message.author.avatar)
                    else:
                        await self.send_global_message(message.guild.name, message.guild.icon, message.content, message.author.display_name, "https://i.ibb.co/D96qZq7/KH75-World-Chat-2.png", footer, fields)
                    # await self.send_global_message(message.content, message.author.display_name,
                    # message.author.avatar
                    await message.delete()
        pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        db = await tools.get_DB_path()
        data = await tools.get_colummn(db, "world_chats", "channel_id")
        print(data)
        for i in data:
            if str(channel.id) == i[0]:
                try:
                    await tools.delete_data(db, "worlds_chats", channel.id)
                    print("global chat deleted")
                    # hier embed senden
                except Exception as e:
                    print(e)


def setup(bot):
    bot.add_cog(GlobalChat(bot))
