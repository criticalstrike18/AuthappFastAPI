from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str 
    email: str
    password: str

 