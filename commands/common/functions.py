# Imported Modules
from common.database.models import *
from common.database.datatypes import *
from sqlalchemy.orm import Session
import logging


# USER ENTITY
def returnUserEntity(data: UserBase, session: Session):
    # queries user entity
    user = session.query(Users).filter_by(discord_id=data.discord_id).first()
    
    if not user:
        # entity doesn't exist; create new entity
        user = Users(discord_id=data.discord_id)
        session.add(user)
        session.commit()
        logging.info(f'[INFO]: User ID ({data.discord_id}) added to the database')

    # returns entity
    logging.info(f'[INFO]: Returned User ID ({data.discord_id}) from the database')
    return user


# SERVER ENITTY
def returnServerEntity(data: ServersBase, session: Session):
    # queries server entity

    server = session.query(Servers).filter_by(server_id=str(data.server_id)).first()

    if not server:
        # entity doesn't exist; create new entity
        server = Servers(server_id=str(data.server_id))
        session.add(server)
        session.commit()
        logging.info(f'[INFO]: Server ID ({data.server_id}) added to the database')

    # returns enity
    logging.info(f'[INFO]: Returned Server ID ({data.server_id}) from the database')
    return server


# SERVERTOUSERS ENTITY
def returnServerToUsersEntity(data: ServersToUsersBase, session: Session):
    # queries servertousers entity
    user_entry = session.query(ServerToUsers).filter_by(discord_id=data.discord_id, server_id=data.server_id).first()

    if not user_entry:
        # entity doesn't exist; create new entity
        user_entry = ServerToUsers(discord_id=data.discord_id, server_id=data.server_id, money=500, banned=False)
        session.add(user_entry)
        session.commit()
        logging.info(f'[INFO]: ServerToUser Line ({data.discord_id}, {data.server_id}) added to the database')

    # returns entity
    logging.info(f'[INFO]: Returned ServerToUser Line ({data.discord_id}, {data.server_id}) from the database')
    return user_entry

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

# ADDS AN ITEM
def returnItem(data: ItemsBase, session: Session):
    # queries Items eneity
    item = session.query(Items).filter_by(item_name=data.item_name,
                                          item_desc=data.item_desc, 
                                          item_value=data.item_value,
                                          item_icon=data.item_icon).first()
    if not item:
        # entity doesn't exist; create new entity
        item = data
        session.add(item)
        session.commit()
        logging.info(f'[INFO]: Item ({item.item_icon}|{item.item_name}) added to the database')
    
    # returns entity
    logging.info(f'[INFO]: Returned Item ({item.item_icon}|{item.item_name}) from the database')
    return item

# GENERATES ALL USABLE ITEMS
def generateItems(session: Session):
    # begins list of items
    returnItem(Items(item_name='Wood', item_desc='Sturdy, reliable, and good for building houses', item_value=50, item_icon='🪵'), session=session)
    returnItem(Items(item_name='Balloon', item_desc='A fun party item', item_value=5, item_icon='🎈'), session=session)