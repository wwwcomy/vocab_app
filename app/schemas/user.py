from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    displayname: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
