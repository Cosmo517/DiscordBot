# Imported Modules
from common.database.models import Users, Servers, ServerToUsers, Items, UserInventory
from sqlalchemy.orm import Session
import logging


# USER ENTITY
def returnUserEntity(data: Users, session: Session):
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
def returnServerEntity(data: Servers, session: Session):
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
def returnServerToUsersEntity(data: ServerToUsers, session: Session):
    # queries servertousers entity
    user_entry = session.query(ServerToUsers).filter_by(discord_id=data.discord_id, server_id=data.server_id).first()

    if not user_entry:
        # entity doesn't exist; create new entity
        user_entry = ServerToUsers(discord_id=data.discord_id, server_id=data.server_id, money=500)
        session.add(user_entry)
        session.commit()
        logging.info(f'[INFO]: ServerToUser Line ({data.discord_id}, {data.server_id}) added to the database')

     # returns entity
    logging.info(f'[INFO]: Returned ServerToUser Line ({data.discord_id}, {data.server_id}) from the database')
    return user_entry


# ADDS AN ITEM
def returnItem(data: Items, session: Session):
    # queries Items eneity
    item = session.query(Items).filter_by(item_name=data.item_name, item_desc=data.item_desc, item_value=data.item_value,
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