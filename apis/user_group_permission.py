from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import UserPermissionSchema
from crud import user_permit_crud
from auth import validate_client_key, validate_active_client


user_permit_router = APIRouter(
    prefix="/user/group/permission",
    tags=["User Group Permission"],
)

@user_permit_router.post('/create', summary="Create Permission for User", status_code=201)
async def create_user_permit(user_permit: UserPermissionSchema, db: Session = Depends(get_db),
                             current_user: dict = Depends(validate_active_client)):
    
    return user_permit_crud.create_user_permit(db, user_permit)
