# Schemas
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator, EmailStr, Field
from typing import List, Optional, Dict, Union, Any
from datetime import datetime

class BaseModel(PydanticBaseModel):
    class config:
        orm_mode = True

class ClientSchema(BaseModel):
    slug: str
    client_key: str   
    
class UpdateStatusSchema(BaseModel):
    status: bool
    
    @validator('status')
    def validate_status(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v
            
class UpdateClientKeySchema(BaseModel):
    client_key: str
    
class ClientCenterSchema(BaseModel):
    center: str
    
class UpdateClientCenterSchema(BaseModel):
    center: str = None
    status: bool = None
class ClientUserSchema(BaseModel):
    username: str
    password: str = Field(min_length=8)
    admin: bool = False
    
    @validator('admin')
    def validate_admin(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v

class UpdateClientUserSchema(BaseModel):
    username: str = None
    group_slug: str = None
    admin: bool = None
    status: bool = None
       
    @validator('admin')
    def validate_admin(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v
        
class refreshTokenSchema(BaseModel):
    refresh_token: str
    
class UpdateClientPasswordSchema(BaseModel):
    password: str
