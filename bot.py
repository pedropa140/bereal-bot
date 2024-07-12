import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
load_dotenv()

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not os.path.exists('images/user_images'):
        os.makedirs('images/user_images')

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.dm_messages = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')
            # bot.loop.create_task()
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message : discord.message.Message):
        if isinstance(message.channel, discord.DMChannel) and message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']):
                    file_path = os.path.join('images/user_images', attachment.filename)
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as response:
                            if response.status == 200:
                                with open(file_path, 'wb') as file:
                                    file.write(await response.read())
                                if (attachment.filename.lower().startswith('img') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('pxl') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('rn_image') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('win') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('photo') and attachment.filename.lower().endswith('.jpg')):
                                    await message.channel.send(f'Image saved as {attachment.filename}. It appears this image may have been taken with Discord\'s camera.')
                                else:
                                    await message.channel.send('Failed to download image.')
                            else:
                                await message.channel.send('Failed to download image.')
                    
    
    # @bot.tree.command(name = "adduser", description = "Adds user to the BeReal-Bot")
    # @app_commands.describe(username = "Username", firstname = 'First Name', lastname = 'Last Name')
    # async def adduser(interaction : discord.Interaction, username : str, firstname : str, lastname : str):
    #     return NotImplementedError

    bot.run(TOKEN)