from asyncio import run
import discord
import asyncio
import requests
import os
from source import dbTools
from source.globalchat import GlobalChat

if not os.path.exists("./source/world.db"):
    asyncio.run(dbTools.create_database("./source/world.db"))
    asyncio.run(dbTools.create_table("./source/world.db", "world_chats", "id, channel_id, webhook_url"))

bot = discord.Bot(
    intents=discord.Intents.all(),
    debug_guilds=["1096186183249305721"])
bot.load_extension("source.globalchat")

# Run the source using the source token
bot.run(run(dbTools.get_DC_token()))
