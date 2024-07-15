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
            filename = ""
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
                                    formatted_time = current_time.strftime("%m%d%YT%H%M%S")
                                    filename = f'images/user_images/{message.author.name}_{formatted_time}.jpg'
                                    with open(filename, 'wb') as file:
                                        file.write(await response.read())
                                    for guild in bot.guilds:
                                        for channel in guild.channels:
                                            if str(channel.name) == 'bereal-bot' and isinstance(channel, discord.ForumChannel):
                                                result_title = f'**{message.author.name} has posted!**'
                                                result_description = f"Posted at {current_time.strftime("%H:%M:%S")}"
                                                embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                                                file = discord.File(f'images/user_images/{message.author.name}_{formatted_time}.jpg', filename=f'{message.author.name}_{formatted_time}.jpg')
                                                embed.set_image(url=f'attachment://{message.author.name}_{formatted_time}.jpg')
                                                embed.set_author(name="bereal-Bot says:")
                                                embed.set_footer(text="/bereal")
                                                
                                                discussion_post = await channel.create_thread(
                                                    name=f"{current_time.strftime("%m/%d/%Y")}: {message.author.name} has posted!",
                                                    content="",
                                                    embed=embed,
                                                    file=file
                                                )
                                                break
                                else:
                                    await message.channel.send('Failed to download image.')
                            else:
                                await message.channel.send('Failed to download image.')
            os.remove(filename)
                    
    
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
