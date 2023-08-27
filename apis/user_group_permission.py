from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import UserPermissionSchema, UserPermissionRemoveSchema
from crud import user_permit_crud
from auth import validate_client_key, validate_active_client


user_permit_router = APIRouter(
    prefix="/user/group/permission",
    tags=["User Group Permission"],
)

@user_permit_router.post('/add', summary="Add Permission for UserGroup", status_code=201)
async def create_user_permit(user_permit: UserPermissionSchema, db: Session = Depends(get_db),
                             current_user: dict = Depends(validate_active_client)):
    
    return user_permit_crud.create_user_permit(db, user_permit)

@user_permit_router.get('/{group_name}', summary="Get all Permissions for UserGroup", status_code=200)
async def get_group_permission(group_name: str, db: Session = Depends(get_db),
                               current_user: dict = Depends(validate_active_client)):
    
    return user_permit_crud.get_group_permissions(db, group_name)


@user_permit_router.delete('/remove', summary="Remove Permissions for UserGroup", status_code=200)
async def remove_permission(user_permit: UserPermissionRemoveSchema, db: Session = Depends(get_db),
                             current_user: dict = Depends(validate_active_client)):
    return user_permit_crud.remove_permission(db, user_permit)
    
