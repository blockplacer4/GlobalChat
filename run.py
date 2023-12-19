from asyncio import run
import discord
import asyncio
import requests
import os
from source import dbTools
from source.globalchat import GlobalChat
from rich.console import Console
import sys

console = Console()

console.print("[[bold green]+[/bold green]] > Checking if Database exists")
if not os.path.exists("./source/world.db"):
    console.print("[[bold yellow]![/bold yellow]] > Creating new database")
    asyncio.run(dbTools.create_database("./source/world.db"))
    console.print("[[bold yellow]![/bold yellow]] > Creating new database table")
    asyncio.run(dbTools.create_table("./source/world.db", "world_chats", "id, channel_id, webhook_url"))

bot = discord.Bot(
    intents=discord.Intents.all(),
    debug_guilds=["1096186183249305721"])


console.print("[[bold green]+[/bold green]] > Setting up Bot Cogs")
bot.load_extension("source.globalchat")

console.print("[[bold green]+[/bold green]] > Access file to get Token")
bot.run(run(dbTools.get_DC_token()))
