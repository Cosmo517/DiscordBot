# Imported modules
from main import db
import common.database.models as models


def returnUserEntity(database: db, discordID: int, serverID: int): # type: ignore
    print("function ran")
    # gets user
    user = db.query(models.ServerToUsers).filter(
        models.ServerToUsers.discord_id == discordID).filter(
        models.ServerToUsers.server_id == serverID).first()
    
    # checks if user exists
    if user:
        # user exists
        return user
    else:
        # user does not exist
        user_to_add = {'discord_id': discordID, 'server_id': serverID}
        db.add(models.ServerToUsers(**user_to_add))
        db.commit()
        return user_to_add
