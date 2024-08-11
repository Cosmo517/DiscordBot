# /commands/money/beg.py
import discord
import random
from discord.ext import commands
from typing import Literal
from common.database.models import Users, ServerToUsers
from common.database.decorator import database_connect
from commands.common.functions import returnUserEntity, returnServerToUsersEntity


# Define the slash command
@database_connect
async def beg_command(interaction: discord.Interaction, session=None):
    discord_id = str(interaction.user.id)
    server_id = str(interaction.guild.id)

    # checks that the user exists
    user = returnUserEntity(Users(discord_id=discord_id), session=session)

    # checks that the servertouser exists
    user_entry = returnServerToUsersEntity(ServerToUsers(discord_id=discord_id, server_id=server_id), session=session)

    # beg logic
    amount = random.randint(0, 100)
    if random.randint(0, 50) == 25:
        amount += random.randint(1, 5000)
    
    # message handling
    msg = ""
    if amount > 100:
        msg = f"SOMEONE ACCIDENTLY DONATED YOU THEIR CREDIT CARD\nEarned: ${amount}"
    else:
        msg = f"Earned: ${amount}"

    # gives the usuer the amount
    user_entry.money += amount
    session.commit()

    # embedded message
    embed = discord.Embed(
        title=f"{interaction.user.display_name} begged for {random.randint(1, 12)} hours...",
        description=msg,
        color=discord.Color.light_grey()
    )

    # send the embedded message
    await interaction.response.send_message(embed=embed)


# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(interaction: discord.Interaction):
        await beg_command(interaction)

    command = discord.app_commands.Command(
        name="beg",
        description="User begs on the streets of discord for spare money",
        callback=wrapper
    )
    bot.tree.add_command(command)