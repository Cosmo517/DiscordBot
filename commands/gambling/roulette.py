# /commands/basic/help.py
import discord
from discord.ext import commands
from typing import Literal
import random as rand
from common.database.models import Users, ServerToUsers
from common.database.decorator import database_connect
from commands.common.functions import returnUserEntity, returnServerToUsersEntity


# Define the slash command
@database_connect
async def roulette_command(interaction: discord.Interaction, amount: int, color: Literal["🔴Red", "⚫Black"], session=None):
    discord_id = str(interaction.user.id)
    server_id = str(interaction.guild.id)

    # checks that the user exists
    user = returnUserEntity(discord_id=discord_id, session=session)

    # checks that the servertouser exists
    user_entry = returnServerToUsersEntity(discord_id=discord_id, server_id=server_id, session=session)

    # balance handling
    current_balance = user_entry.money
    if amount > current_balance:
        await interaction.response.send_message(f"Insufficient funds! Your current balance is ${current_balance}.", ephemeral=True)
        return

    # roulette logic
    red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    green_numbers = {0, 37}
    rand_num = rand.randint(0, 37)
    color_val = discord.Color.blurple()
    color_name = "default"

    # determine the result color
    if rand_num in green_numbers:
        color_val = discord.Color.green()
        color_name = "🍏Green"
    elif rand_num in red_numbers:
        color_val = discord.Color.red()
        color_name = "🔴Red"
    else:
        color_val = discord.Color.dark_grey()
        color_name = "⚫Black"

    # determine win or loss
    if color == color_name:
        winnings = amount
        user_entry.money += winnings
    else:
        losses = amount
        user_entry.money -= losses

    # commit the updated balance to the database
    session.commit()

    # embedded message
    embed = discord.Embed(
        title="🛞Roulette Game",
        description=f"Amount Bet: ${amount} on {color}",
        color=color_val
    )
    embed.add_field(name="RESULTS:", value=f"{rand_num} {color_name}", inline=False)

    if color == color_name:
        embed.add_field(name="WINNINGS:", value=f"${amount}")
    else:
        embed.add_field(name="LOSSES:", value=f"${amount}")

    embed.set_footer(text="One gamble away from winning!")

    # send the embedded message
    await interaction.response.send_message(embed=embed)


# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    async def wrapper(interaction: discord.Interaction, amount: int, color: Literal["🔴Red", "⚫Black"]):
        await roulette_command(interaction, amount, color)

    command = discord.app_commands.Command(
        name="roulette",
        description="ALL ON BLACK",
        callback=wrapper
    )
    bot.tree.add_command(command)