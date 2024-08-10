# /Commands/Gambling/blackjack.py
import discord
from discord.ext import commands

# Define the slash command
async def blackjack_command(interaction: discord.Interaction):
    """
    blackjack... money

    Parameters: None
    Returns: None
    """

    # Embeded message
    embed = discord.Embed(
        title="Blackjack",
        description="MONEY",
        color=discord.Color.dark_gray()
    )
    embed.set_footer(text="GAMBLE YOUR CHILD'S COLLEGE MONEY, BLACKJACKKKKK") # footer

    await interaction.response.send_message(embed=embed)

# Set up the command in the bot's command tree
async def setup(bot: commands.Bot):
    # Create a slash command
    command = discord.app_commands.Command(
        name="blackjack",
        description="Money",
        callback=blackjack_command
    )
    bot.tree.add_command(command)