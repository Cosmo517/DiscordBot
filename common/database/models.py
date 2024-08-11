from sqlalchemy import Column, Integer, BigInteger, String, Float, ForeignKey
from common.database.database import Base

# Create the users table
class Users(Base):
    __tablename__ = "users"
    discord_id = Column(String(30), primary_key=True, index=True)

# Create the servers table
class Servers(Base):
    __tablename__ = "servers"
    server_id = Column(String(30), primary_key=True, index=True)
    admin_role = Column(String(30), nullable=True)

# Create the items table
class Items(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(25), nullable=False)
    item_desc = Column(String(256), nullable=True)
    item_value = Column(Integer, nullable=True)
    item_icon = Column(String(3), nullable=False)

# Create the table to store the servers a user is in
class ServerToUsers(Base):
    __tablename__ = "servertousers"
    discord_id = Column(String(30), ForeignKey('users.discord_id'), primary_key=True)
    server_id = Column(String(30), ForeignKey('servers.server_id'), primary_key=True)
    money = Column(Integer, nullable=False)

# Create a table to store the users inventory
class UserInventory(Base):
    __tablename__ = "userinventory"
    server_id = Column(String(30), ForeignKey('servers.server_id'), primary_key=True)
    discord_id = Column(String(30), ForeignKey('users.discord_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)