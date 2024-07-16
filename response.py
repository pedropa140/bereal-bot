import discord
from discord import app_commands
from discord.ext import commands
import json
import sqlite3
import os

from user import User, UserDatabase

async def add_user(interaction : discord.Interaction, firstname : str, lastname : str, userdatabase : UserDatabase):
    if not userdatabase.user_id_exists(interaction.user.id):
        new_user = User(interaction.user.name, int(interaction.user.id), firstname, lastname)
        new_user.to_json()
        userdatabase.insert_user(interaction.user.name, int(interaction.user.id), firstname, lastname)
        result_title = f'**User Created**'
        result_description = f'Account for user <@{new_user.get_user_id(interaction.user.name, firstname, lastname)}> has been created.'
        embed = discord.Embed(title=result_title, description=result_description, color=8311585)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_image(url='attachment://icon.png')
        embed.set_author(name="bereal-Bot says:")
        embed.set_footer(text="/adduser")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
    else:
        result_title = f'**ERROR**'
        result_description = f'USER **{interaction.user.name}** DOES NOT EXIST IN DATABASE'
        embed = discord.Embed(title=result_title, description=result_description, color=13632027)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_image(url='attachment://icon.png')
        embed.set_author(name="bereal-Bot says:")
        embed.set_footer(text="/adduser")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

async def remove_user(interaction : discord.Interaction, userdatabase : UserDatabase):
    if not userdatabase.user_id_exists(interaction.user.id):
        result_title = f'**ERROR**'
        result_description = f'USER **{interaction.user.name}** DOES NOT EXIST IN DATABASE'
        embed = discord.Embed(title=result_title, description=result_description, color=13632027)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_image(url='attachment://icon.png')
        embed.set_author(name="bereal-Bot says:")
        embed.set_footer(text="/removeuser")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
    else:
        if os.path.exists(f'user_info/{interaction.user.id}_bereal.JSON'):
            os.remove(f'user_info/{interaction.user.id}_bereal.JSON')
        userdatabase.delete_user(interaction.user.id)
        result_title = f'**User Deleted**'
        result_description = f'Account for **{interaction.user.mention}** has been deleted'
        embed = discord.Embed(title=result_title, description=result_description, color=8311585)
        file = discord.File('images/icon.png', filename='icon.png')
        embed.set_image(url='attachment://icon.png')
        embed.set_author(name="bereal-Bot says:")
        embed.set_footer(text="/removeuser")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)