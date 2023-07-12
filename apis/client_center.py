from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import (
    ClientUserSchema, 
    UpdateClientUserSchema,
    refreshTokenSchema,
    UpdateClientUserSchema
)
from crud import user_crud
from db import models
from auth import validate_client_key
from auth import validate_active_client
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

center_router = APIRouter(
    prefix="/center",
    tags=["Client Center"],
)

@center_router.post('/create', summary="Create a Center for a client", status_code=201)
async def create_center(db: Session = Depends(get_db), 
                        current_user: models.ClientUsers = Depends(validate_active_client)):
    return "yes"
