# Imported Modules
from common.database.models import Users, Servers, ServerToUsers
from sqlalchemy.orm import Session
import logging


# USER ENTITY
def returnUserEntity(discord_id: str, session: Session):
    # queries user entity
    user = session.query(Users).filter_by(discord_id=discord_id).first()
    
    if not user:
        # entity doesn't exist; create new entity
        user = Users(discord_id=discord_id)
        session.add(user)
        session.commit()
        logging.info(f'[INFO]: User ID ({discord_id}) added to the database')

    # returns entity
    logging.info(f'[INFO]: Returned User ID ({discord_id}) from the database')
    return user


# SERVER ENITTY
def returnServerEntity(server_id: str, session: Session):
    # queries server entity
    server = session.query(Servers).filter_by(server_id=str(server_id)).first()
    if not server:
        # entity doesn't exist; create new entity
        server = Servers(server_id=str(server_id))
        session.add(server)
        session.commit()
        logging.info(f'[INFO]: Server ID ({server_id}) added to the database')

    # returns enity
    logging.info(f'[INFO]: Returned Server ID ({server_id}) from the database')
    return server


# SERVERTOUSERS ENTITY
def returnServerToUsersEntity(discord_id: str, server_id: str, session: Session):
    # queries servertousers entity
    user_entry = session.query(ServerToUsers).filter_by(discord_id=discord_id, server_id=server_id).first()

    if not user_entry:
        # entity doesn't exist; create new entity
        user_entry = ServerToUsers(discord_id=discord_id, server_id=server_id, money=500)
        session.add(user_entry)
        session.commit()
        logging.info(f'[INFO]: ServerToUser Line ({discord_id}, {server_id}) added to the database')

     # returns entity
    logging.info(f'[INFO]: Returned ServerToUser Line ({discord_id}, {server_id}) from the database')
    return user_entry