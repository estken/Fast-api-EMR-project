from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import sys
from typing import List
sys.path.append("..")
from db.session import get_db
from schema import UserPermissionSchema
from crud import user_permit_crud
from auth import validate_active_client


user_permit_router = APIRouter(
    prefix="/user/group/permission",
    tags=["User Group Permission"],
)

@user_permit_router.post('/add', summary="Add Permission for UserGroup", status_code=201)
async def create_user_permit(user_permit: UserPermissionSchema, db: Session = Depends(get_db),
                             current_user: dict = Depends(validate_active_client)):
    
    return user_permit_crud.create_user_permit(db, user_permit)

@user_permit_router.get('/{group_slug}', summary="Get all Permissions for UserGroup", status_code=200)
async def get_group_permission(group_slug: str, db: Session = Depends(get_db),
                               current_user: dict = Depends(validate_active_client)):
    
    return user_permit_crud.get_group_permissions(db, group_slug)


@user_permit_router.delete('/remove/{group_slug}', summary="Remove Permissions for UserGroup", status_code=200)
async def remove_permission(group_slug: str, router_name: List[str] = Query(...), db: Session = Depends(get_db),
                             current_user: dict = Depends(validate_active_client)):
    return user_permit_crud.remove_permission(db, group_slug, router_name)
    
