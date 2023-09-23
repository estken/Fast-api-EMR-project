import sys
sys.path.append("..")
from schema import BaseModel
from pydantic import validator


class GenderSchema(BaseModel):
    name: str
    
class GenderUpdateSchema(BaseModel):
    name: str = None
    status: bool = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v