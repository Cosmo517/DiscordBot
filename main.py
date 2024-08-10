# Imported Modules
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from common.database.database import SessionLocal, engine
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
import common.database.models as models

# Setting up variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Setting up DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# To use the database in other files, import db_dependency
# then add "db: db_dependency" to the parameters of a function
# afterwards, you can use db to query the database, as well as insert new objects
db_dependency = Annotated[Session, Depends(get_db)]

# Create all the tables
models.Base.metadata.create_all(bind=engine)

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
