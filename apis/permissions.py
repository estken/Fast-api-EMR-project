from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import PermissionSchema, UpdatePermissionSchema
from crud import permit_crud
from auth import validate_active_client


permission_router = APIRouter(
    prefix="/permission",
    tags=["Permission"],
)

@permission_router.post('/create', summary="Create Permissions", status_code=200)
async def create_permission(create_permit: PermissionSchema, current_user: dict = Depends(validate_active_client), 
                            db: Session = Depends(get_db)):
    
    return permit_crud.create_permission(db, create_permit)

@permission_router.patch('/enable/{router_name}', summary="Enable a permission", status_code=200)
async def enable_permission(router_name: str, 
                            current_user: dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    update_permit_data = {
        'status': True
    }
    return permit_crud.update_permit(db, router_name, update_permit_data)

@permission_router.patch('/disable/{router_name}', summary="Disable a permission", status_code=200)
async def enable_permission(router_name: str, 
                            current_user: dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    update_permit_data = {
        'status': False
    }
    return permit_crud.update_permit(db, router_name, update_permit_data)

@permission_router.get('/enabled', summary="Get all Enabled Permissions", status_code=200)
async def enabled_permission(page: int=Query(1, ge=1), 
                         page_size:int =10, 
                         current_user: dict = Depends(validate_active_client),db: Session = Depends(get_db)):
    
    return permit_crud.get_permissions(db, page, page_size, True)

@permission_router.get('/', summary="Get all Permissions", status_code=200)
async def all_permission(page: int=Query(1, ge=1), 
                         page_size:int =10, current_user: dict = Depends(validate_active_client), 
                         db: Session = Depends(get_db)):
    
    return permit_crud.get_permissions(db, page, page_size)

@permission_router.patch('/update/{router_name}', summary="Update Permission", status_code=200)
async def all_permission(router_name: str, update_permit_data: UpdatePermissionSchema, current_user: dict = Depends(validate_active_client), 
                            db: Session = Depends(get_db)):
    
    return permit_crud.update_permit(db, router_name, update_permit_data.dict(exclude_unset=True, exclude_none=True))