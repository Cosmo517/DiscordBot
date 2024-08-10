# /Commands/Basic/help.py
import discord
from discord.ext import commands

# Define the slash command
async def help_command(interaction: discord.Interaction):
    """
    Prompts a message explaining how the bot works and the available commands

    Parameters: None
    Returns: None
    """

    # Embeded message
    embed = discord.Embed(
        title="CosmoBot Help",
        description="Here's how to use the bot:",
        color=discord.Color.green()
    )
    embed.add_field(name="Big Text?", value="I think this is little text?", inline=False) # field
    embed.set_footer(text="If you read this, then stuff is working... yay") # footer

    # Sends the embded message
    await interaction.response.send_message(embed=embed)

# Adds the command to the slash command list
async def setup(bot: commands.Bot):
    command = discord.app_commands.Command(
        name="help",
        description="Provides informational slides regarding how the bot works",
        callback=help_command
    )
    bot.tree.add_command(command)
