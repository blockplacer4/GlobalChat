import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncpg
import aiohttp

import run
from source import dbTools
from configparser import ConfigParser
import os

class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_session = aiohttp.ClientSession()

    async def send_global(self, message):
        for url in await dbTools.get_colummn("./source/world.db", "world_chats", "webhook_url"):
            await self.webhook_session.post(url, json={"content": message.content,
                                                        "username": message.author.name,
                                                        "avatar_url": message.author.avatar_url})

    async def send_global_message(self, message):
        for url in await dbTools.get_colummn("./source/world.db", "world_chats", "webhook_url"):
            await self.webhook_session.post(url, json={"content": str(message)})

    async def get_webhook(self, channel_id):
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return None
            webhooks = await channel.webhooks()
            webhook = discord.utils.get(webhooks, name="GlobalChat")
            if not webhook:
                webhook = await channel.create_webhook(name="GlobalChat")
            return webhook.url
        except Exception as e:
            print(e.with_traceback(e))

    async def deletewebhook(self, channel_id):
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return None
            webhooks = await channel.webhooks()
            webhook = discord.utils.get(webhooks, name="GlobalChat")
            if webhook:
                webhook = await channel.delete_webhook(name="GlobalChat")
        except Exception as e:
            print(e.with_traceback(e))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("No Permission, yk yk.")

    @discord.slash_command()
    async def addglobal(self, ctx, channel: discord.TextChannel):
        # async with self.bot.pool.acquire() as conn:
        if await dbTools.view_dat_row(await dbTools.get_DB_path(), "world_chats", "channel_id", channel.id):
            await ctx.respond(
                f"{channel.mention} ist bereits ein global chat zum entfernen benutze /removeglobal <channel>")
        else:
            webhook = await self.get_webhook(channel.id)
            await ctx.respond(f"{channel.mention} wurde zum Global Chat hinzugefügt.")
            try:
                db = await dbTools.get_DB_path()
                id = await dbTools.get_next_id(db, "world_chats")
                await dbTools.insert_data(db, "world_chats", id, channel.id, webhook)
            except Exception as e:
                print(e.with_traceback(e))

    @discord.slash_command()
    async def removeglobal(self, ctx, channel: discord.TextChannel):
        # async with self.bot.pool.acquire() as conn:
        db = await dbTools.get_DB_path()
        await dbTools.delete_data(db, "world_chats", f"{channel.id}")
        await self.deletewebhook(channel.id)
        await ctx.respond(f"{channel.mention} wurde vom Global Chat entfernt.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            db = await dbTools.get_DB_path()
            print(message.channel.id)
            await self.send_global_message(message)
        pass


def setup(bot):
    bot.add_cog(GlobalChat(bot))
