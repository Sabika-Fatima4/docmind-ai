from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str