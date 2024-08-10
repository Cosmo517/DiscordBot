# Imported Modules
import os
import discord
from discord.ext import commands
import operator
from dotenv import load_dotenv

# Setting up variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initating Slash Commands
@bot.event
async def on_ready():
    """
    Function that sets up the command tree and imported commands of sub-folder python scripts

    Parameters: None
    Returns: None
    """

    # Guild varaible stuff (The server ID)
    guild_id = 1271479998154543114
    guild = discord.Object(id=guild_id)

    # Loads the extensions (commands)
    await bot.load_extension('commands.basic.help')
    await bot.load_extension('commands.gambling.blackjack')

    # Sets up the command tree
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    # Confirms the commands are loaded and synced
    print(f'Logged in as {bot.user} and commands are synced for server {guild_id}')

# Runs the bot
bot.run(TOKEN)
