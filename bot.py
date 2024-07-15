import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

import json
from dotenv import load_dotenv
import response
from user import User, UserDatabase
import datetime
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
    userdatabase = UserDatabase('users_database.db')

    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')            
            print(f'{bot.user} is now running!')
            # bot.loop.create_task()
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message : discord.message.Message):
        if isinstance(message.channel, discord.DMChannel) and message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as response:
                            if response.status == 200:
                                contents = None
                                with open(f'user_info/{message.author.id}_bereal.JSON', 'r') as file:
                                    contents = json.load(file)
                                if attachment.filename in contents['filenames']:
                                    await message.channel.send(f'File already uploaded to {bot.user}')
                                    break
                                if (attachment.filename.lower().startswith('img') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('pxl') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('rn_image') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('win') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('photo') and attachment.filename.lower().endswith('.jpg')):
                                    with open(f'user_info/{message.author.id}_bereal.JSON', 'w') as file:
                                        contents['filenames'].append(attachment.filename)
                                        json.dump(contents, file, indent=4)
                                        await message.channel.send(f'Image saved as {attachment.filename}.')
                                    current_time = datetime.datetime.now()
                                    current_time = current_time.strftime("%m%d%YT%H%M%S")
                                    with open(f'images/user_images/{message.author.name}_{current_time}.jpg', 'wb') as file:
                                        file.write(await response.read())
                                    # for guild in bot.guilds:
                                    #     for channel in guild.channels:
                                    #         if channel.name == 'bereal-bot' and channel.type == 'fourm':

                                else:
                                    await message.channel.send('Failed to download image.')
                            else:
                                await message.channel.send('Failed to download image.')
                    
    
    @bot.tree.command(name = "adduser", description = "Adds user to the BeReal-Bot")
    @app_commands.describe(firstname = 'First Name', lastname = 'Last Name')
    async def adduser(interaction : discord.Interaction, firstname : str, lastname : str):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.add_user(bot, interaction, firstname, lastname, userdatabase)

    @bot.tree.command(name = "removeuser", description = "Removes a user from BeReal-Bot")
    async def removeuser(interaction : discord.Interaction):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.remove_user(bot, interaction, userdatabase)

    bot.run(TOKEN)
