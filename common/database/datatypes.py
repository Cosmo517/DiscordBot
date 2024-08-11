from pydantic import BaseModel

# The below classes are used to make objects to insert into the database

class UserBase(BaseModel):
    discord_id: str

class ServersBase(BaseModel):
    server_id: str
    admin_role: str

class ItemsBase(BaseModel):
    item_id: int
    item_nam: str
    item_desc: str
    item_value: int

class ServersToUsersBase(BaseModel):
    discord_id: str
    server_id: str
    money: int

class UserInventoryBase(BaseModel):
    discord_id: str
    item_id: int
    quantity: int