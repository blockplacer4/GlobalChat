import discord
from discord.ext import commands
import asyncio
import requests
import os

intents = discord.Intents.default()
intents.messages = True  # Needed to read and send messages
intents.webhooks = True  # Needed for webhook requests
intents.message_content = True


class ListeningCog(commands.Cog, name='MessageListener'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        channel_id = ''  # Replace with the actual channel ID
        print('Listening for messages in channel ID:', channel_id)

        while True:
            recent_messages = await self.bot.cached_messages(self.bot.user.server_channels[0])
            recent_message = recent_messages[-1]

            if recent_message.channel.id != channel_id:
                continue

            await self.bot.delete_message(recent_message)
            webhook_url = ''
            webhook_data = {
                'content': recent_message.content
            }

            response = requests.post(webhook_url, json=webhook_data)

            if response.status_code == 200:
                print('Message sent successfully to Discord')
            else:
                print('Failed to send message to Discord:', response.text)

            await asyncio.sleep(60)  # 60 seconds


bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(ListeningCog(bot))

# Read the bot token from the environment variable
bot_token = "[token]"

# Run the bot using the bot token
bot.run(bot_token)
