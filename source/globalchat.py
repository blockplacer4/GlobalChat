import discord
from discord.ext import commands
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
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return None
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name="GlobalChat")
        if not webhook:
            webhook = await channel.create_webhook(name="GlobalChat")
        return webhook.url

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("No Permission, yk yk.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        async with self.bot.pool.acquire() as conn:
            records = await conn.fetch("SELECT channel_id FROM global_channels")
        for record in records:
            if message.channel.id == record["channel_id"]:
                webhook = await self.get_webhook(record["channel_id"])
                if webhook:
                    async with self.webhook_session.post(webhook.url, json={"content": message.content,
                                                                            "username": message.author.name,
                                                                            "avatar_url": message.author.avatar_url}) as response:
                        pass

    @commands.command()
    @commands.has_permissions(manage_webhooks=True)
    async def addglobal(self, ctx, channel: discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            webhook = self.get_webhook(channel.id)
            db = await dbTools.get_DB_path()
            id = await dbTools.get_next_id(db, "globalchat")
            await dbTools.insert_data(db, "globalchat", id, channel.id, webhook)
        await ctx.send(f"{channel.mention} wurde zum Global Chat hinzugefügt.")

    @commands.command()
    @commands.has_permissions(manage_webhooks=True)
    async def removeglobal(self, ctx, channel: discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            db = await dbTools.get_DB_path()
            webhook = self.get_webhook(channel.id)
            rows = await dbTools.view_data(db, "globalchat", 1)
            for row in rows:
                if row[1] == channel.id:
                    await dbTools.delete_data(db, "globalchat", f"id={row[0]}")
        await ctx.send(f"{channel.mention} wurde vom Global Chat entfernt.")


def setup(bot):
    bot.add_cog(GlobalChat(bot))
