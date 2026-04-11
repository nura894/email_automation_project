from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name:str = Field(..., min_length=1, max_length=100)
    email : EmailStr= Field(...)
    password: str = Field(..., min_length =4, max_length=64)
    smtp_password: str = Field(...)


class UserResponse(BaseModel):
    id: int
    name : str
    email : EmailStr

    class Config:
        from_attributes= True
        
 # use to update the data
        
class UpdateUserRequest(BaseModel):
    name : Optional[str] = Field(None, min_length=1, max_length=100)
    password : Optional[str] = Field( None, min_length =4, max_length=64)
    smtp_password : Optional[str]  
    
    