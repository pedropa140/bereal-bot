import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import os

import json
import random
import asyncio
from dotenv import load_dotenv
import response
from user import User, UserDatabase
import datetime
import time
load_dotenv()

user_dict = {}
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
    for user in userdatabase.get_all_user_ids():
            if user not in user_dict:
                user_dict[user] = False
    random_datetime = None

    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {synced} command(s)')
            print(f'Synced {len(synced)} command(s)')            
            print(f'{bot.user} is now running!')
            bot.loop.create_task(ping_at_specific_time(bot, user_dict))
        except Exception as e:
            print(e)

    async def ping_at_specific_time(bot : commands.Bot, user_dict : dict):
        global random_datetime
        datetime_variable = datetime.datetime.now()
        if int(datetime_variable.hour) + 1 > 20:
            hour = 10
        else:
            hour = int(datetime_variable.hour) + 1
        random_hour = random.randint(hour, 20)
        random_minute = random.randint(0, 59)
        random_string = f'{random_hour:02d}:{random_minute:02d}'
        current_date = datetime.datetime.now().date()
        random_time = datetime.datetime.strptime(random_string, '%H:%M').time()
        random_datetime = datetime.datetime.combine(current_date, random_time)
        time_string = '10:00:00'
        time_object = datetime.datetime.strptime(time_string, '%H:%M:%S').time()
        combined_datetime = datetime.datetime.combine(datetime_variable.date(), time_object)
        while True:
            for user in userdatabase.get_all_user_ids():
                if user not in user_dict:
                    user_dict[user] = False
            datetime_variable = datetime.datetime.now()
            datetime_time = datetime_variable.strftime('%H:%M')
            datetime_time = datetime.datetime.strptime(datetime_time, '%H:%M').time()
            current_datetime = datetime.datetime.combine(datetime_variable, datetime_time)
            combined_datetime = datetime.datetime.combine(datetime_variable.date(), time_object)
            print('--------------------------------------------------')
            print(f'CURRENT TIME: \t\t{current_datetime}')
            print(f'PING RESTART: \t\t{combined_datetime}')
            print(f'PING TIME: \t\t{random_datetime}')
            if current_datetime == combined_datetime:
                random_hour = random.randint(11, 19)
                random_minute = random.randint(0, 59)
                random_string = f'{random_hour:02d}:{random_minute:02d}'
                current_date = datetime.datetime.now().date()
                random_time = datetime.datetime.strptime(random_string, '%H:%M').time()
                random_datetime = datetime.datetime.combine(current_date, random_time)
                print(f'NEW PING TIME: \t\t{random_datetime}')
            
            print('--------------------------------------------------')
            # if current_datetime == random_datetime:
            if current_datetime == current_datetime:
                for guild in bot.guilds:
                    print(f'Guild Name: {guild.name}')
                    for channel in guild.channels:
                        if channel.name == 'bereal-bot' and str(channel.type) == 'forum':
                            print(f'Channel Name: {channel.name}')
                            for thread in channel.threads:
                                await thread.delete()
                    print(user_dict)
                    for user in user_dict:
                        print(f'User: {user}')
                        bereal_id = 0
                        guild = bot.get_guild(int(guild.id))
                        if guild:
                            for role in guild.roles:
                                if role.name == 'bereal-user':
                                    print(f'ROLE ID: {role.id}')
                                    bereal_id = role.id
                                    break

                        role = guild.get_role(int(bereal_id))
                        if role:
                            try:
                                member = guild.get_member(user)
                                if member is None:
                                    member = await guild.fetch_member(user)
                                    print(f'Member : {member}')
                                if member:
                                        await member.remove_roles(role)
                            except:
                                continue

                for user in user_dict:
                    user_dict[user] = False
                result_title = f'**BeReal Time!**'
                result_description = f"You have ***3*** Minutes to post your BeReal!"
                embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                embed.set_image(url=f'attachment://icon.png')
                embed.set_author(name="bereal-Bot says:")
                embed.set_footer(text="/bereal")

                for user in user_dict:
                    send_message = await bot.fetch_user(user)
                    with open('images/icon.png', 'rb') as f:
                        file = discord.File(f, filename='icon.png')
                        await send_message.send(file=file, embed=embed)

            await asyncio.sleep(60)

    @bot.event
    async def on_message(message : discord.message.Message):
        global random_datetime
        global user_dict
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
                                    result_title = f'**ERROR**'
                                    result_description = f'File {attachment.filename} already uploaded to {bot.user}'
                                    embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                    file = discord.File('images/icon.png', filename='icon.png')
                                    embed.set_image(url='attachment://icon.png')
                                    embed.set_author(name="bereal-Bot says:")
                                    embed.set_footer(text="/removeuser")
                                    await message.channel.send(file=file, embed=embed)
                                    break
                                if user_dict[message.author.id] != True:
                                    if ((attachment.filename.lower().startswith('img') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('pxl') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('rn_image') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('win') and attachment.filename.lower().endswith('.jpg')) or (attachment.filename.lower().startswith('photo') and attachment.filename.lower().endswith('.jpg'))):
                                        with open(f'user_info/{message.author.id}_bereal.JSON', 'w') as file:
                                            contents['filenames'].append(attachment.filename)
                                            json.dump(contents, file, indent=4)
                                            result_title = f'**Image Uploaded**'
                                            result_description = f'Image saved as {attachment.filename}.'
                                            embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                                            file = discord.File('images/icon.png', filename='icon.png')
                                            embed.set_image(url='attachment://icon.png')
                                            embed.set_author(name="bereal-Bot says:")
                                            embed.set_footer(text="/removeuser")
                                            await message.channel.send(file=file, embed=embed)
                                        current_time = datetime.datetime.now()
                                        formatted_time = current_time.strftime("%m%d%YT%H%M%S")
                                        filename = f'images/user_images/{message.author.id}_{formatted_time}.jpg'
                                        with open(filename, 'wb') as file:
                                            file.write(await response.read())
                                        for guild in bot.guilds:
                                            for channel in guild.channels:
                                                if str(channel.name) == 'bereal-bot' and isinstance(channel, discord.ForumChannel):
                                                    result_title = f'**{message.author.id} has posted!**'                                                    
                                                    result_description = f"Posted at {current_time.strftime('%H:%M:%S')}"
                                                    time_to_add = datetime.timedelta(minutes=3)
                                                    time_difference = current_time - (random_datetime + time_to_add)
                                                    if time_difference.total_seconds() > 0:
                                                        if time_difference.total_seconds() >= 3600:
                                                            hours = int(time_difference.total_seconds() / 3600)
                                                            hour_label = "hour" if hours == 1 else "hours"
                                                            result_description += f' ({hours} {hour_label} late)'
                                                        elif time_difference.total_seconds() >= 60:
                                                            minutes = int(time_difference.total_seconds() / 60)
                                                            minute_label = "minute" if minutes == 1 else "minutes"
                                                            result_description += f' ({minutes} {minute_label} late)'
                                                        else:
                                                            seconds = int(time_difference.total_seconds())
                                                            second_label = "second" if seconds == 1 else "seconds"
                                                            result_description += f' ({seconds} {second_label} late)'

                                                    embed = discord.Embed(title=result_title, description=result_description, color=8311585)
                                                    file = discord.File(f'images/user_images/{message.author.id}_{formatted_time}.jpg', filename=f'{message.author.id}_{formatted_time}.jpg')
                                                    embed.set_image(url=f'attachment://{message.author.id}_{formatted_time}.jpg')
                                                    embed.set_author(name="bereal-Bot says:")
                                                    embed.set_footer(text="/bereal")
                                                    
                                                    discussion_post = await channel.create_thread(
                                                        name=f"{current_time.strftime('%m/%d/%Y')}: {message.author.name} has posted!",
                                                        content="",
                                                        embed=embed,
                                                        file=file
                                                    )
                                                    break
                                        user_dict[message.author.id] = True
                                        for guild in bot.guilds:
                                            bereal_id = 0
                                            guild = bot.get_guild(int(guild.id))
                                            if guild:
                                                for role in guild.roles:
                                                    if role.name == 'bereal-user':
                                                        bereal_id = role.id
                                                        break

                                            role = guild.get_role(int(bereal_id))
                                            if role:
                                                member = guild.get_member(message.author.id)
                                                if member is None:
                                                    member = await guild.fetch_member(message.author.id)
                                                if member:
                                                    await member.add_roles(role)
                                    else:
                                        result_title = f'**ERROR**'
                                        result_description = 'Incorrect file format.'
                                        embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                        file = discord.File('images/icon.png', filename='icon.png')
                                        embed.set_image(url='attachment://icon.png')
                                        embed.set_author(name="bereal-Bot says:")
                                        embed.set_footer(text="/removeuser")
                                        await message.channel.send(file=file, embed=embed)
                                else:
                                    result_title = f'**ERROR**'
                                    result_description = 'You have already posted a BeReal.'
                                    embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                    file = discord.File('images/icon.png', filename='icon.png')
                                    embed.set_image(url='attachment://icon.png')
                                    embed.set_author(name="bereal-Bot says:")
                                    embed.set_footer(text="/removeuser")
                                    await message.channel.send(file=file, embed=embed)
                            else:
                                result_title = f'**ERROR**'
                                result_description = 'Failed to download image.'
                                embed = discord.Embed(title=result_title, description=result_description, color=13632027)
                                file = discord.File('images/icon.png', filename='icon.png')
                                embed.set_image(url='attachment://icon.png')
                                embed.set_author(name="bereal-Bot says:")
                                embed.set_footer(text="/removeuser")
                                await message.channel.send(file=file, embed=embed)
            try:
                os.remove(filename)
            except Exception as e:
                pass                    
    
    @bot.tree.command(name = "adduser", description = "Adds user to the BeReal-Bot")
    async def adduser(interaction : discord.Interaction):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.add_user(interaction, userdatabase)
        global user_dict
        for user in userdatabase.get_all_user_ids():
            if user not in user_dict:
                user_dict[user] = False

    @bot.tree.command(name = "removeuser", description = "Removes a user from BeReal-Bot")
    async def removeuser(interaction : discord.Interaction):
        username = str(interaction.user)
        mention = str(interaction.user.mention)
        user_message = str(interaction.command.name)
        channel = str(interaction.channel)
        
        print(f'{username} ({mention}) said: "{user_message}" ({channel})')

        await response.remove_user(interaction, userdatabase)

    bot.run(TOKEN)
