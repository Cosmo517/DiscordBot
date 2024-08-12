# Imported Modules
from common.database.models import *
from common.database.datatypes import *
from commands.common.functions import returnUserEntity, returnServerEntity, returnServerToUsersEntity
from sqlalchemy.orm import Session
import logging

# Adds a warn to the user when the warn command is used.
def addUserWarn(data: WarnsBase, session: Session):
    # Make sure the user exists in each table
    user = returnUserEntity(Users(discord_id=data.discord_id), session=session)
    server = returnServerEntity(Servers(server_id=data.server_id), session=session)
    server_to_user = returnServerToUsersEntity(ServerToUsers(discord_id=data.discord_id, server_id=data.server_id, money=0), session=session)
    
    if user and server and server_to_user:
        session.add(Warns(discord_id=data.discord_id, server_id=data.server_id, reason=data.reason))
        session.commit()
        logging.info(f'[INFO]: Added a warning for user {data.discord_id} on server {data.server_id} with reason {data.reason}')
        return True
    else:
        logging.warning(f"[WARNING]: Failed to add user, server, or server_to_user with: {data} while adding a warning")
        return False

# Return all the warns a user has
def returnUserWarnings(data: WarnsBase, session: Session):
    warns = session.query(Warns).filter_by(discord_id=data.discord_id,
                                           server_id=data.server_id).all()
    return warns

# Ban a user
def banUser(data: BansBase, session: Session):
    user = returnUserEntity(Users(discord_id=data.discord_id), session=session)
    server = returnServerEntity(Servers(server_id=data.server_id), session=session)
    if user and server:
        session.add(Bans(discord_id=data.discord_id, server_id=data.server_id, reason=data.reason))
        session.commit()
        logging.info(f'[INFO]: Banned user {data.discord_id} in server {data.server_id} for reason {data.reason}')
        return True
    else:
        logging.warning(f'[WARNING]: Failed to ban user {data.discord_id} in server {data.server_id} for reason {data.reason}')
        return False

# Check if a user is banned
def isBanned(data: BansBase, session: Session):
    user = session.query(Bans).filter_by(discord_id=data.discord_id,
                                         server_id=data.server_id).first()
    return user if user else False
