import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncpg
import aiohttp
from source import dbTools
from configparser import ConfigParser
import os


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_session = aiohttp.ClientSession()

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

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("No Permission, yk yk.")

    @discord.slash_command()
    async def addglobal(self, ctx, channel: discord.TextChannel):
        print("/addglobal was used")
        # async with self.bot.pool.acquire() as conn:
        print(channel.id)
        webhook = await self.get_webhook(channel.id)
        await ctx.respond(f"{channel.mention} wurde zum Global Chat hinzugefügt.")
        print(channel.id)
        try:
            db = await dbTools.get_DB_path()
            await ctx.send("1")
            id = await dbTools.get_next_id(db, "world_chats")
            await ctx.send(id)
            await dbTools.insert_data(db, "world_chats", id, channel.id, webhook)
            await ctx.send("3")
        except Exception as e:
            print(e.with_traceback(e))

    @discord.slash_command()
    async def removeglobal(self, ctx, channel: discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            db = await dbTools.get_DB_path()
            webhook = self.get_webhook(channel.id)
            rows = await dbTools.view_data(db, "world_chats", 1)
            for row in rows:
                if row[1] == channel.id:
                    await dbTools.delete_data(db, "world_chats", f"id={row[0]}")
        await ctx.respond(f"{channel.mention} wurde vom Global Chat entfernt.")

def setup(bot):
    bot.add_cog(GlobalChat(bot))
