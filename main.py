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
from common.database.database import SessionLocal
from common.database.models import Servers

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
# models.Base.metadata.create_all(bind=engine)

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
        server_entry = session.query(Servers).filter_by(server_id=str(guild_id)).first()
        
        if not server_entry:
            # no server found, add it to the list
            new_server = Servers(server_id=str(guild_id))
            session.add(new_server)
            session.commit()
            print(f"Server ID ({guild_id}) added to the database")
        else:
            # server already exists
            print(f"Server ID ({guild_id}) already exists in the database")

    except Exception as e:
        # an error occured while querying
        print(f"An error occurred while checking/adding server ID: {e}")

    finally:
        # closes the session
        session.close()

    # loads in the extension modules (command python files)
    await bot.load_extension('commands.basic.help')
    await bot.load_extension('commands.gambling.blackjack')
    await bot.load_extension('commands.basic.test')
    await bot.load_extension('commands.gambling.roulette')

    # sets up the command tree
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    # verifies everything is logged in and synced
    print(f'Logged in as {bot.user} and commands are synced for server {guild_id}')

# runs the bot
bot.run(TOKEN)
