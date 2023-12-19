import discord
from discord.ext import commands
import asyncio
import requests
import os
from source import dbTools
from source import globalchat

if not os.path.exists("./source/world.db"):
    asyncio.run(dbTools.create_database("./source/world.db"))
    asyncio.run(dbTools.create_table("./source/world.db", "world_chats", "id, channel_id, webhook_url"))

bot = discord.Bot(intents=discord.Intents.all())
bot.load_extension("Cogs.globalchat")


# Run the source using the source token
bot.run(dbTools.get_DC_token())
