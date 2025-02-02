from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import UserGroupSchema, UpdateUserGroupSchema
from crud import group_crud
from auth import validate_client_key, validate_active_client


user_group_router = APIRouter(
    prefix="/user/group",
    tags=["User Group"],
)

@user_group_router.post("/create", summary="Create a single user group", 
                        status_code=201)
async def create_group(user_data: UserGroupSchema, current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    return group_crud.create_user_group(db, user_data)

@user_group_router.patch("/disable/{slug}", summary="Disable a user group for a client", status_code=200)
async def disable_group(slug: str, current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):    
    update_data = {
        "status": False
    }
    return group_crud.update_group(db, slug, update_data)

@user_group_router.patch("/enable/{slug}", summary="Enable a user group for a client", status_code=200)
async def enable_group(slug: str, current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    
    update_data = {
        "status": True
    }
    return group_crud.update_group(db, slug, update_data)

@user_group_router.patch("/update/{slug}", summary="Update a user group data for a client", status_code=200)
async def update_group(slug: str, update_data: UpdateUserGroupSchema, current_user:dict = Depends(validate_active_client), 
                        db: Session = Depends(get_db)):
    
    return group_crud.update_group_data(db, slug, update_data)

@user_group_router.get('/', summary="Get all user groups per client", status_code=200)
async def view_all(current_user:dict = Depends(validate_active_client), page: int=Query(1, ge=1), 
                   page_size:int =10, db: Session = Depends(get_db)):
    
    return group_crud.get_groups(db, page, page_size)

@user_group_router.get('/enabled', summary="Get all enabled user groups", status_code=200)
async def view_enabled(current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    
    return group_crud.get_enabled(db)

@user_group_router.get('/single/{slug}', summary="View Single User Group", status_code=200)
async def view_single(slug: str, current_user:dict = Depends(validate_active_client), db:Session = Depends(get_db)):
    
    return group_crud.single_group(db, slug)