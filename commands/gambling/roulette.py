# /commands/gambling.roulette.py
import discord
from discord.ext import commands
from typing import Literal
import random as rand
#import commands.common.command_functions as c_funct

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
    rand_num = rand.randint(0, 37)
    color_val = discord.Color.blurple()
    color_name = "default"

    # the user
    #db_user = await returnUserEntity(interaction.user.id, interaction.guild.id)
    #print(db_user.discord_id, db_user.server_id)

    # sets col, col_name to the correct values
    if rand_num in green_numbers:
        # is green
        color_val = discord.Color.green()
        color_name = "🍏Green"
    elif rand_num in red_numbers:
        # is red
        color_val = discord.Color.red()
        color_name = "🔴Red"
    else:
        # is black
        color_val = discord.Color.dark_grey()
        color_name = "⚫Black"

    # Embeded message
    embed = discord.Embed(
        title="🛞Roulette Game",
        description=f"Amount Bet: ${amount} on {color}",
        color=color_val
    )

    # adds the fields for the results
    embed.add_field(name="RESULTS:", value=f"{rand_num} {color_name}", inline=False)

    if color == color_name:
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