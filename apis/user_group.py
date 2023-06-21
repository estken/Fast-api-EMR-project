from fastapi import APIRouter, Depends, Request, Response, HTTPException, Query
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import UserGroupSchema, UpdateUserGroupSchema
from crud import group_crud
from db import models
from auth import validate_client_key
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

user_group_router = APIRouter(
    prefix="/user_group",
    tags=["User Group"],
)

@user_group_router.post("/create", summary="Create a single user group", 
                        status_code=201, dependencies=[Depends(validate_client_key)], name="user_group_create")
async def create_group(request: Request, user_data: UserGroupSchema, db: Session = Depends(get_db)):
    # get the client id fromt the middleware.
    client_id = request.state.data
    # get the name of the route.
    route_name = request.scope['route'].name
    return group_crud.create_user_group(db, client_id, user_data, route_name)

@user_group_router.patch("/disable/{user_group_id}", summary="Disable a user group for a client", status_code=200,
                                                dependencies=[Depends(validate_client_key)], name="user_group_disable")
async def disable_group(request:Request, user_group_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    # get the name of the route.
    route_name = request.scope['route'].name
    
    update_data = {
        "status": False
    }
    return group_crud.update_group(db, client_id, user_group_id, update_data, route_name)

@user_group_router.patch("/enable/{user_group_id}", summary="Enable a user group for a client", status_code=200,
                                                dependencies=[Depends(validate_client_key)], name="user_group_enable")
async def enable_group(request:Request, user_group_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    # get the name of the route.
    route_name = request.scope['route'].name
    
    update_data = {
        "status": True
    }
    return group_crud.update_group(db, client_id, user_group_id, update_data, route_name)
