# Imported Modules
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from common.database.database import SessionLocal, engine
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
import logging
from common.database.models import Servers, Base
from commands.common.functions import returnServerEntity, generateItems

# debugging
logging.basicConfig(level=logging.DEBUG)
############

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
Base.metadata.create_all(bind=engine)


# Initating Slash Commands
@bot.event
async def on_ready():
    """
    Function that sets up the command tree and imported commands of sub-folder python scripts

    Parameters: None
    Returns: None
    """

    # guild variables (stuff for ServerID)
    guild_id = 1271479998154543114
    guild = discord.Object(id=guild_id)

    # opens the datababse session
    session = SessionLocal()

    try:
        # queries, looking for the server
        server_entry = returnServerEntity(Servers(server_id=guild_id), session=session)

        # generates all the items for the bot
        generateItems(session=session)

    except Exception as e:
        # an error occured while querying
        logging.error(f'An error occurred while running main.py database content: {e}')

    finally:
        # closes the session
        session.close()

    # loads in the extension modules (command python files)
    await bot.load_extension('commands.basic.help')
    await bot.load_extension('commands.gambling.blackjack')
    await bot.load_extension('commands.basic.test')
    await bot.load_extension('commands.gambling.roulette')
    await bot.load_extension('commands.money.balance')
    await bot.load_extension('commands.money.beg')
    await bot.load_extension('commands.staff.kick')

    # sets up the command tree
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    # verifies everything is logged in and synced
    logging.info(f'Logged in as {bot.user} and commands are synced for server {guild_id}')

# runs the bot
bot.run(TOKEN)
