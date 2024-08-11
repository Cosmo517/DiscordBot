from common.database.models import Users, Servers, ServerToUsers
from sqlalchemy.orm import Session

def returnUserEntity(discord_id: str, session: Session):
    user = session.query(Users).filter_by(discord_id=discord_id).first()
    if not user:
        user = Users(discord_id=discord_id)
        session.add(user)
        session.commit()
        print(f"User ID ({discord_id}) added to the database")
    print(f"Returned User ID ({discord_id}) from the database")
    return user

def returnServerEntity(server_id: str, session: Session):
    server = session.query(Servers).filter_by(server_id=str(server_id)).first()
    if not server:
        server = Servers(server_id=str(server_id))
        session.add(server)
        session.commit()
        print(f"Server ID ({server_id}) added to the database")
    print(f"Returned Server ID ({server_id}) from the database")
    return server

def returnServerToUsersEntity(discord_id: str, server_id: str, session: Session):
    user_entry = session.query(ServerToUsers).filter_by(discord_id=discord_id, server_id=server_id).first()
    if not user_entry:
        user_entry = ServerToUsers(discord_id=discord_id, server_id=server_id, money=500)
        session.add(user_entry)
        session.commit()
        print(f"ServerToUser Line ({discord_id}, {server_id}) added to the database")
    print(f"Returned ServerToUser Line ({discord_id}, {server_id}) from the database")
    return user_entry