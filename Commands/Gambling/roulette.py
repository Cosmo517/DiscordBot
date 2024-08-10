# /commands/basic/help.py
import discord
from discord.ext import commands
from typing import Literal
import random as r

# Define the slash command
async def roulette_command(interaction: discord.Interaction, amount: int, color: Literal["🔴Red", "⚫Black"]):
    """
    Gambling Command. Selects a random number 1 - 38
    if it is: {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}, then it is Red
    if it is: {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}, then it is Black
    if it is: {0, 37}, then it is Green

    if it matches the pre-selected color, the user wins double what they invested
    else, they lose everything

    Green is a loss no matter what because you can only invest in Red/Black

    Parameters: None
    Returns: None
    """
    # variables
    red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    green_numbers = {0, 37}
    rand_num = r.randint(0, 37)
    col = discord.Color.blurple()
    col_name = "purp"

    # sets col, col_name to the correct values
    if rand_num in green_numbers:
        # is green
        col = discord.Color.green()
        col_name = "🍏Green"
    elif rand_num in red_numbers:
        # is red
        col = discord.Color.red()
        col_name = "🔴Red"
    else:
        # is black
        col = discord.Color.dark_grey()
        col_name = "⚫Black"

    # Embeded message
    embed = discord.Embed(
        title="🛞Roulette Game",
        description=f"Amount Bet: ${amount} on {color}",
        color=col
    )

    # adds the fields for the results
    embed.add_field(name="RESULTS:", value=f"{rand_num} {col_name}", inline=False)

    if color == col_name:
        embed.add_field(name="WINNINGS:", value=F"${amount}")
    else:
        embed.add_field(name="LOSSES:", value=F"${amount}")

    embed.set_footer(text="One gamble away from winning!")

    # Sends the embded message
    await interaction.response.send_message(embed=embed)

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    command = discord.app_commands.Command(
        name="roulette",
        description="ALL ON BLACK",
        callback=roulette_command
    )
    bot.tree.add_command(command)