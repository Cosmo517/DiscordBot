# /commands/basic/help.py
import discord
from discord.ext import commands

# Define the slash command
async def test_command(interaction: discord.Interaction, user: discord.User, amount: int):
    """
    Test command for practicing new features

    Parameters: None
    Returns: None
    """

    # Embeded message
    embed = discord.Embed(
        title="🛠️|Test Command",
        description=f"The user 🙍{user.display_name} was beaten with a 🏒stick x{amount} times!",
        color=discord.Color.blurple()
    )
    #embed.add_field(name="Test Test", value="test test test", inline=False) # field
    embed.set_footer(text="test test test test test test") # footer

    # Sends the embded message
    await interaction.response.send_message(embed=embed)

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    command = discord.app_commands.Command(
        name="test",
        description="Tests stuff",
        callback=test_command
    )
    bot.tree.add_command(command)
