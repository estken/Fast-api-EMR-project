from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import (
    UserSchema,
    UserCenterSchema,
    UserDefaultSchema
)
from crud import center_crud, user_center_crud
from db import client_model as models
from auth import validate_client_key
from auth import validate_active_client
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

user_center_router = APIRouter(
    prefix="/user/center",
    tags=["User Center"],
)

@user_center_router.get('/', summary="Get all centers from a user", status_code=200)
async def get_user_centers(user: UserSchema, db: Session = Depends(get_db), 
                           current_user: dict = Depends(validate_active_client)):
    
    return user_center_crud.get_user_centers(db, user, current_user)

@user_center_router.post('/add', summary="add new centers for user", status_code=200)
async def add_new_centers(user_center: UserCenterSchema, db: Session = Depends(get_db), 
                          current_user: dict = Depends(validate_active_client)):
    
    return user_center_crud.add_new_center(db, user_center, current_user)

@user_center_router.delete('/remove', summary="remove centers from user", status_code=200)
async def remove_centers(user_center: UserCenterSchema, db: Session = Depends(get_db), 
                          current_user: dict = Depends(validate_active_client)):
    
    return user_center_crud.remove_center(db, user_center, current_user)

@user_center_router.patch('/activate', summary="Set Center as Default for user", status_code=200)
async def set_default(user_center: UserDefaultSchema, db: Session = Depends(get_db),
                      current_user: dict = Depends(validate_active_client)):
    
    return user_center_crud.set_default_center(db, user_center, current_user)

