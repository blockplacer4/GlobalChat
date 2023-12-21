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

    async def send_global_message(self, server_name: str, author_icon: str, message: str, author: str, avatar_url: str, footer: dict, fields: list):
        for url in await tools.get_colummn("./source/world.db", "world_chats", "webhook_url"):
            webhook = Webhook.from_url(str(url), session=self.webhook_session)
            e = await tools.create_embed(server_name, author_icon, author, message, avatar_url, footer, fields)
            a = e.copy()
            await webhook.send(embed=e)

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
        # async with self.bot.pool.acquire() as conn:
        if await tools.view_dat_row(await tools.get_DB_path(), "world_chats", "channel_id", channel.id):
            await ctx.respond(
                f"{channel.mention} ist bereits ein global chat zum entfernen benutze /removeglobal <channel>")
        else:
            webhook = await self.get_webhook(channel.id)
            await ctx.respond(f"{channel.mention} wurde zum Global Chat hinzugefügt.")
            try:
                db = await tools.get_DB_path()
                id = await tools.get_next_id(db, "world_chats")
                await tools.insert_data(db, "world_chats", id, channel.id, webhook)
            except Exception as e:
                print(e.with_traceback(e))

    @discord.slash_command()
    async def removeglobal(self, ctx, channel: discord.TextChannel):
        # async with self.bot.pool.acquire() as conn:
        db = await tools.get_DB_path()
        await tools.delete_data(db, "world_chats", f"{channel.id}")
        await self.deletewebhook(channel.id)
        await ctx.respond(f"{channel.mention} wurde vom Global Chat entfernt.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            for channel_id in await tools.get_colummn("./source/world.db", "world_chats", "channel_id"):
                if int(channel_id[0]) == message.channel.id:
                    db = await tools.get_DB_path()
                    url = urlparse('https://world.killerhase75.com')
                    footer = {
                        "icon_url": self.bot.user.avatar,
                        "text": f"Server anzahl: {await run.get_server_count()}"
                    }
                    fields = [
                        {'name': '', 'value': '🤖 [Invite mich](https://world.killerhase75.com)', 'inline': True}
                    ]
                    print(message.author.avatar)

                    await self.send_global_message(message.guild.name, message.guild.icon, message.content, message.author.display_name, message.author.avatar.url, footer, fields)
                    # await self.send_global_message(message.content, message.author.display_name,
                    # message.author.avatar)
                    await message.delete()
        pass


def setup(bot):
    bot.add_cog(GlobalChat(bot))
