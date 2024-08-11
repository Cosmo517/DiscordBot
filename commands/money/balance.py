# /commands/money/balance.py
import discord
from discord.ext import commands
from typing import Literal
from common.database.decorator import database_connect
from commands.common.functions import returnUserEntity, returnServerToUsersEntity


# Define the slash command
@database_connect
async def balance_command(interaction: discord.Interaction, session=None):
    discord_id = str(interaction.user.id)
    server_id = str(interaction.guild.id)

    # checks that the user exists
    user = returnUserEntity(discord_id=discord_id, session=session)

    # checks that the servertouser exists
    user_entry = returnServerToUsersEntity(discord_id=discord_id, server_id=server_id, session=session)

    # embedded message
    embed = discord.Embed(
        title="💰Account Balance",
        description=f"Balance: ${user_entry.money}",
        color=discord.Color.green()
    )

    # send the embedded message
    await interaction.response.send_message(embed=embed)


# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(interaction: discord.Interaction):
        await balance_command(interaction)

    command = discord.app_commands.Command(
        name="balance",
        description="Displays current balance of the user",
        callback=wrapper
    )
    bot.tree.add_command(command)